"""Browser automation plugin - Search Google, open URLs, etc."""

import logging
import platform
import subprocess
import webbrowser
from typing import Dict, Any
from urllib.parse import quote

logger = logging.getLogger(__name__)

class BrowserPlugin:
    """Browser automation and search"""
    
    NAME = "browser"
    DESCRIPTION = "Browser automation: search Google, open URLs"
    TRIGGERS = ["search", "google", "browse", "open url"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute browser command"""
        try:
            command_lower = command.lower().strip()
            
            if "search" in command_lower or "google" in command_lower:
                query = args.get("query", "")
                if not query:
                    # Extract query from command
                    query = command_lower.replace("search", "").replace("google", "").strip()
                
                if query:
                    url = f"https://www.google.com/search?q={quote(query)}"
                    webbrowser.open(url)
                    return {
                        "status": "success",
                        "message": f"Searching Google for: {query}",
                        "url": url
                    }
                else:
                    return {
                        "status": "error",
                        "message": "No search query provided"
                    }
            
            elif "open" in command_lower or "url" in command_lower:
                url = args.get("url", "")
                if not url:
                    return {
                        "status": "error",
                        "message": "No URL provided"
                    }
                
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                
                webbrowser.open(url)
                return {
                    "status": "success",
                    "message": f"Opening URL: {url}",
                    "url": url
                }
            
            return {
                "status": "error",
                "message": "Unknown browser command"
            }
        
        except Exception as e:
            logger.error(f"Browser command error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
