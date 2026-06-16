"""Command processing and routing for Aji OS plugins"""

import logging
from typing import Dict, Any, Optional
import importlib
import inspect
from pathlib import Path

logger = logging.getLogger(__name__)

class CommandRouter:
    """Route commands to appropriate plugins"""
    
    def __init__(self):
        """Initialize command router"""
        self.plugins: Dict[str, Any] = {}
        self.command_map: Dict[str, str] = {}  # command -> plugin_name
        self._load_plugins()
    
    def _load_plugins(self) -> None:
        """Load all plugins from plugins directory"""
        plugins_dir = Path(__file__).parent / "plugins"
        
        if not plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {plugins_dir}")
            return
        
        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                module_name = f"plugins.{plugin_file.stem}"
                module = importlib.import_module(module_name)
                
                # Find plugin classes
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, "NAME"):
                        plugin_name = obj.NAME
                        self.plugins[plugin_name] = obj
                        
                        # Register triggers
                        if hasattr(obj, "TRIGGERS"):
                            for trigger in obj.TRIGGERS:
                                self.command_map[trigger.lower()] = plugin_name
                        
                        logger.info(f"Loaded plugin: {plugin_name}")
            
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file.name}: {e}")
    
    async def route_command(self, command: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route command to appropriate plugin"""
        args = args or {}
        command_lower = command.lower().strip()
        
        # Check direct command match
        plugin_name = self.command_map.get(command_lower)
        
        if not plugin_name:
            # Try partial match
            for trigger, p_name in self.command_map.items():
                if trigger in command_lower or command_lower in trigger:
                    plugin_name = p_name
                    break
        
        if not plugin_name:
            return {
                "status": "error",
                "message": f"Command not recognized: {command}",
                "available_commands": list(self.command_map.keys())
            }
        
        plugin_class = self.plugins.get(plugin_name)
        if not plugin_class:
            return {
                "status": "error",
                "message": f"Plugin not found: {plugin_name}"
            }
        
        try:
            if hasattr(plugin_class, "execute"):
                result = await plugin_class.execute(command, args)
                return result
            else:
                return {
                    "status": "error",
                    "message": f"Plugin {plugin_name} has no execute method"
                }
        
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_available_commands(self) -> Dict[str, list]:
        """Get all available commands"""
        result = {}
        
        for trigger, plugin_name in self.command_map.items():
            if plugin_name not in result:
                result[plugin_name] = []
            result[plugin_name].append(trigger)
        
        return result
    
    def get_plugin_info(self, plugin_name: str) -> Dict[str, Any]:
        """Get information about a plugin"""
        plugin_class = self.plugins.get(plugin_name)
        
        if not plugin_class:
            return {"error": f"Plugin not found: {plugin_name}"}
        
        return {
            "name": getattr(plugin_class, "NAME", plugin_name),
            "description": getattr(plugin_class, "DESCRIPTION", ""),
            "triggers": getattr(plugin_class, "TRIGGERS", []),
            "available_commands": [
                trigger for trigger, p_name in self.command_map.items()
                if p_name == plugin_name
            ]
        }

# Global command router instance
command_router = CommandRouter()
