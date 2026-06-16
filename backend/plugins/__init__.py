"""Aji OS Plugin System

Plugins provide modular, extensible functionality for system control and automation.
Each plugin implements a standard interface for command execution.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class PluginBase:
    """Base class for all Aji OS plugins"""
    
    NAME: str = "base"
    DESCRIPTION: str = "Base plugin template"
    TRIGGERS: list = []
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plugin command
        
        Args:
            command: The command to execute
            args: Additional arguments
            
        Returns:
            Result dictionary with status, data, and optional message
        """
        raise NotImplementedError("Plugin must implement execute method")
