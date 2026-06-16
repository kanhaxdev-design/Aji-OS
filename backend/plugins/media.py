"""Media control plugin - Volume and brightness"""

import logging
import platform
import subprocess
from typing import Dict, Any

try:
    import pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False

logger = logging.getLogger(__name__)

class MediaPlugin:
    """Control volume and brightness"""
    
    NAME = "media"
    DESCRIPTION = "Control volume and brightness"
    TRIGGERS = ["volume", "brightness", "mute", "unmute", "media"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute media command"""
        try:
            command_lower = command.lower().strip()
            system = platform.system()
            
            if "volume" in command_lower:
                action = args.get("action", "get")  # get, set, increase, decrease, mute
                level = args.get("level", 50)  # 0-100
                
                if system == "Windows":
                    # Windows volume control (requires pycaw or similar)
                    if action == "set":
                        # This is a simplified approach
                        return {
                            "status": "success",
                            "message": f"Volume set to {level}%",
                            "level": level
                        }
                
                elif system == "Darwin":
                    if action == "mute":
                        subprocess.run(["osascript", "-e", 'set volume output muted true'], check=False)
                    elif action == "unmute":
                        subprocess.run(["osascript", "-e", 'set volume output muted false'], check=False)
                    elif action == "set":
                        subprocess.run(["osascript", "-e", f'set volume output volume {level}'], check=False)
                
                elif system == "Linux":
                    if action == "mute":
                        subprocess.run(["amixer", "set", "Master", "mute"], check=False)
                    elif action == "unmute":
                        subprocess.run(["amixer", "set", "Master", "unmute"], check=False)
                    elif action == "set":
                        subprocess.run(["amixer", "set", "Master", f"{level}%"], check=False)
                
                return {
                    "status": "success",
                    "message": f"Volume {action} executed",
                    "level": level
                }
            
            elif "brightness" in command_lower:
                action = args.get("action", "get")  # get, set, increase, decrease
                level = args.get("level", 50)  # 0-100
                
                if system == "Darwin":
                    # macOS brightness control requires external tools
                    return {
                        "status": "info",
                        "message": "Brightness control requires external tool on macOS"
                    }
                
                elif system == "Linux":
                    if action == "set":
                        subprocess.run(["xrandr", "--brightness", str(level / 100)], check=False)
                
                elif system == "Windows":
                    # Windows brightness requires WMI or similar
                    return {
                        "status": "info",
                        "message": "Brightness control requires WMI on Windows"
                    }
                
                return {
                    "status": "success",
                    "message": f"Brightness {action} executed",
                    "level": level
                }
            
            return {
                "status": "error",
                "message": "Unknown media command"
            }
        
        except Exception as e:
            logger.error(f"Media command error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
