"""VS Code launcher plugin"""

import logging
import platform
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VSCodePlugin:
    """Launch VS Code and open files/folders"""
    
    NAME = "vscode"
    DESCRIPTION = "Launch VS Code and open projects"
    TRIGGERS = ["vscode", "code", "visual studio", "open vscode"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute VS Code command"""
        try:
            system = platform.system()
            path = args.get("path", "")
            
            if system == "Windows":
                if path:
                    subprocess.Popen(["code", path])
                else:
                    subprocess.Popen(["code"])
            
            elif system == "Darwin":
                if path:
                    subprocess.Popen(["open", "-a", "Visual Studio Code", path])
                else:
                    subprocess.Popen(["open", "-a", "Visual Studio Code"])
            
            elif system == "Linux":
                if path:
                    subprocess.Popen(["code", path])
                else:
                    subprocess.Popen(["code"])
            
            return {
                "status": "success",
                "message": f"VS Code launched{' opening: ' + path if path else ''}"
            }
        
        except Exception as e:
            logger.error(f"VS Code launch error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
