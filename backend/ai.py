"""AI orchestration for Aji OS"""

import logging
from typing import AsyncGenerator, Optional, List, Dict, Any
from providers import get_provider
from memory import memory
from config import settings

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """Manage AI interactions and context"""
    
    def __init__(self):
        """Initialize AI orchestrator"""
        self.current_provider = settings.default_provider
        self.provider_instance = None
        self._init_provider()
    
    def _init_provider(self) -> None:
        """Initialize current provider"""
        try:
            self.provider_instance = get_provider(self.current_provider)
            logger.info(f"AI provider initialized: {self.current_provider}")
        except Exception as e:
            logger.error(f"Failed to initialize AI provider: {e}")
    
    def set_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider"""
        try:
            test_provider = get_provider(provider_name)
            self.current_provider = provider_name
            self.provider_instance = test_provider
            logger.info(f"Switched to provider: {provider_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to switch provider to {provider_name}: {e}")
            return False
    
    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from AI"""
        
        if not self.provider_instance:
            yield "Error: AI provider not initialized"
            return
        
        # Add user message to memory
        memory.add_message(
            role="user",
            content=message,
            conversation_id=conversation_id
        )
        
        # Get conversation context
        context = memory.get_context(conversation_id)
        
        # Use provided system prompt or default
        system = system_prompt or settings.ai_system_prompt
        
        # Stream response from provider
        response_text = ""
        try:
            async for chunk in self.provider_instance.chat(message, context, system):
                response_text += chunk
                yield chunk
        
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            yield f"Error: {str(e)}"
            return
        
        # Add assistant response to memory
        memory.add_message(
            role="assistant",
            content=response_text,
            conversation_id=conversation_id
        )
    
    async def chat_sync(self, message: str, conversation_id: Optional[str] = None) -> str:
        """Get complete AI response (non-streaming)"""
        
        if not self.provider_instance:
            return "Error: AI provider not initialized"
        
        # Add user message to memory
        memory.add_message(
            role="user",
            content=message,
            conversation_id=conversation_id
        )
        
        # Get conversation context
        context = memory.get_context(conversation_id)
        
        try:
            response = await self.provider_instance.chat_sync(message, context)
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            response = f"Error: {str(e)}"
        
        # Add assistant response to memory
        memory.add_message(
            role="assistant",
            content=response,
            conversation_id=conversation_id
        )
        
        return response
    
    def get_conversation_context(self, conversation_id: Optional[str] = None) -> List[Dict[str, str]]:
        """Get conversation context"""
        return memory.get_context(conversation_id)
    
    def create_conversation(self) -> str:
        """Create new conversation"""
        return memory.create_conversation()
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return ["groq", "gemini", "openai", "ollama"]
    
    def get_current_provider(self) -> str:
        """Get current provider name"""
        return self.current_provider

# Global AI orchestrator instance
ai_orchestrator = AIOrchestrator()
