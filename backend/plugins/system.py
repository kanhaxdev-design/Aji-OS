"""System control plugin - Shutdown, restart, sleep, lock, etc."""

import logging
import platform
import subprocess
import psutil
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SystemPlugin:
    """System control commands"""
    
    NAME = "system"
    DESCRIPTION = "System control: shutdown, restart, sleep, lock"
    TRIGGERS = ["shutdown", "restart", "sleep", "lock", "system"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system command"""
        try:
            command_lower = command.lower().strip()
            system = platform.system()
            
            if "shutdown" in command_lower:
                if system == "Windows":
                    subprocess.run(["shutdown", "/s", "/t", "0"], check=False)
                elif system in ["Darwin", "Linux"]:
                    subprocess.run(["sudo", "shutdown", "-h", "now"], check=False)
                return {
                    "status": "success",
                    "message": "Shutdown initiated"
                }
            
            elif "restart" in command_lower:
                if system == "Windows":
                    subprocess.run(["shutdown", "/r", "/t", "0"], check=False)
                elif system in ["Darwin", "Linux"]:
                    subprocess.run(["sudo", "shutdown", "-r", "now"], check=False)
                return {
                    "status": "success",
                    "message": "Restart initiated"
                }
            
            elif "sleep" in command_lower:
                if system == "Windows":
                    subprocess.run(["rundll32.exe", "powrprof.dll", "SetSuspendState", "0", "1", "0"], check=False)
                elif system == "Darwin":
                    subprocess.run(["osascript", "-e", "tell application \"System Events\" to sleep"], check=False)
                elif system == "Linux":
                    subprocess.run(["systemctl", "suspend"], check=False)
                return {
                    "status": "success",
                    "message": "Sleep mode activated"
                }
            
            elif "lock" in command_lower:
                if system == "Windows":
                    subprocess.run(["rundll32.exe", "user32.dll", "LockWorkStation"], check=False)
                elif system == "Darwin":
                    subprocess.run(["osascript", "-e", "tell application \"System Events\" to keystroke \"q\" using {command down, control down}"], check=False)
                elif system == "Linux":
                    subprocess.run(["gnome-screensaver-command", "-l"], check=False)
                return {
                    "status": "success",
                    "message": "Screen locked"
                }
            
            return {
                "status": "error",
                "message": "Unknown system command"
            }
        
        except Exception as e:
            logger.error(f"System command error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            battery = psutil.sensors_battery()
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "battery_percent": battery.percent if battery else None,
                "is_plugged": battery.power_plugged if battery else None
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {}
