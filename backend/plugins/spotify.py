"""Spotify launcher plugin"""

import logging
import platform
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpotifyPlugin:
    """Launch Spotify and control playback"""
    
    NAME = "spotify"
    DESCRIPTION = "Launch Spotify music player"
    TRIGGERS = ["spotify", "music", "play music", "open spotify"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Spotify command"""
        try:
            system = platform.system()
            
            if system == "Windows":
                # Spotify URI scheme: spotify:track:trackid
                subprocess.Popen(["spotify.exe"])
            
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", "Spotify"])
            
            elif system == "Linux":
                subprocess.Popen(["spotify"])
            
            return {
                "status": "success",
                "message": "Spotify launched"
            }
        
        except Exception as e:
            logger.error(f"Spotify launch error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
