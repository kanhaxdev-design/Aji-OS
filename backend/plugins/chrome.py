"""Chrome launcher plugin"""

import logging
import platform
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ChromePlugin:
    """Launch Chrome and perform browser actions"""
    
    NAME = "chrome"
    DESCRIPTION = "Launch Chrome browser and manage tabs"
    TRIGGERS = ["chrome", "open chrome", "browser"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Chrome command"""
        try:
            system = platform.system()
            url = args.get("url", "")
            
            if system == "Windows":
                chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                if url:
                    subprocess.Popen([chrome_path, url])
                else:
                    subprocess.Popen([chrome_path])
            
            elif system == "Darwin":
                if url:
                    subprocess.Popen(["open", "-a", "Google Chrome", url])
                else:
                    subprocess.Popen(["open", "-a", "Google Chrome"])
            
            elif system == "Linux":
                if url:
                    subprocess.Popen(["google-chrome", url])
                else:
                    subprocess.Popen(["google-chrome"])
            
            return {
                "status": "success",
                "message": f"Chrome launched{' with URL: ' + url if url else ''}"
            }
        
        except Exception as e:
            logger.error(f"Chrome launch error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
