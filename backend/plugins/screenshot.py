"""Screenshot plugin"""

import logging
from typing import Dict, Any
from pathlib import Path

try:
    from PIL import ImageGrab
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

logger = logging.getLogger(__name__)

class ScreenshotPlugin:
    """Take screenshots"""
    
    NAME = "screenshot"
    DESCRIPTION = "Take screenshot and save to file"
    TRIGGERS = ["screenshot", "take screenshot", "capture", "screen"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute screenshot command"""
        if not HAS_PIL:
            return {
                "status": "error",
                "message": "PIL not installed. Install with: pip install Pillow"
            }
        
        try:
            # Create screenshots directory
            screenshots_dir = Path("./data/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = screenshots_dir / f"screenshot_{timestamp}.png"
            
            # Take screenshot
            screenshot = ImageGrab.grab()
            screenshot.save(str(filename))
            
            logger.info(f"Screenshot saved: {filename}")
            
            return {
                "status": "success",
                "message": f"Screenshot saved to {filename}",
                "file_path": str(filename)
            }
        
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
