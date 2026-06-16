"""Calculator plugin"""

import logging
import re
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CalculatorPlugin:
    """Simple calculator functionality"""
    
    NAME = "calculator"
    DESCRIPTION = "Perform mathematical calculations"
    TRIGGERS = ["calculate", "calc", "math", "compute"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute calculator command"""
        try:
            expression = args.get("expression") or command
            
            # Remove common words
            expression = expression.lower().replace("calculate", "").replace("what is", "").strip()
            
            # Sanitize expression - only allow safe characters
            if not re.match(r'^[\d\s\+\-\*/\(\)\.]+$', expression):
                return {
                    "status": "error",
                    "message": "Invalid expression. Only numbers and basic operators allowed."
                }
            
            # Evaluate expression safely
            try:
                result = eval(expression)
                return {
                    "status": "success",
                    "expression": expression,
                    "result": result,
                    "message": f"{expression} = {result}"
                }
            except ZeroDivisionError:
                return {
                    "status": "error",
                    "message": "Cannot divide by zero"
                }
        
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
