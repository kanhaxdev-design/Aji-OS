"""AI Provider implementations for Aji OS"""

import logging
from typing import Optional, AsyncGenerator
from abc import ABC, abstractmethod
from config import settings

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Base class for all AI providers"""
    
    @abstractmethod
    async def chat(
        self,
        message: str,
        conversation_history: list = None,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Send message and stream response"""
        pass
    
    @abstractmethod
    async def chat_sync(self, message: str, conversation_history: list = None) -> str:
        """Send message and get complete response (non-streaming)"""
        pass


class GroqProvider(AIProvider):
    """Groq AI Provider - Primary provider for Aji OS"""
    
    def __init__(self):
        """Initialize Groq provider"""
        try:
            from groq import Groq, AsyncGroq
            self.client = Groq(api_key=settings.groq_api_key)
            self.async_client = AsyncGroq(api_key=settings.groq_api_key)
        except ImportError:
            logger.error("Groq library not installed. Install with: pip install groq")
            raise
    
    async def chat(
        self,
        message: str,
        conversation_history: list = None,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from Groq"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            stream = self.async_client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            yield f"Error: {str(e)}"
    
    async def chat_sync(self, message: str, conversation_history: list = None) -> str:
        """Non-streaming response from Groq"""
        try:
            messages = []
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = self.client.chat.completions.create(
                model=settings.default_model,
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return f"Error: {str(e)}"


class GeminiProvider(AIProvider):
    """Google Gemini AI Provider"""
    
    def __init__(self):
        """Initialize Gemini provider"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            logger.error("Google Generative AI library not installed. Install with: pip install google-generativeai")
            raise
    
    async def chat(
        self,
        message: str,
        conversation_history: list = None,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from Gemini"""
        try:
            import google.generativeai as genai
            
            model = genai.GenerativeModel('gemini-pro')
            chat = model.start_chat(history=conversation_history or [])
            response = chat.send_message(message, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            yield f"Error: {str(e)}"
    
    async def chat_sync(self, message: str, conversation_history: list = None) -> str:
        """Non-streaming response from Gemini"""
        try:
            import google.generativeai as genai
            
            model = genai.GenerativeModel('gemini-pro')
            chat = model.start_chat(history=conversation_history or [])
            response = chat.send_message(message)
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return f"Error: {str(e)}"


class OpenAIProvider(AIProvider):
    """OpenAI GPT AI Provider"""
    
    def __init__(self):
        """Initialize OpenAI provider"""
        try:
            from openai import AsyncOpenAI, OpenAI
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.async_client = AsyncOpenAI(api_key=settings.openai_api_key)
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
    
    async def chat(
        self,
        message: str,
        conversation_history: list = None,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from OpenAI"""
        try:
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            stream = self.async_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            yield f"Error: {str(e)}"
    
    async def chat_sync(self, message: str, conversation_history: list = None) -> str:
        """Non-streaming response from OpenAI"""
        try:
            messages = []
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Error: {str(e)}"


class OllamaProvider(AIProvider):
    """Ollama Local AI Provider - For offline use"""
    
    def __init__(self):
        """Initialize Ollama provider"""
        import requests
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.requests = requests
    
    async def chat(
        self,
        message: str,
        conversation_history: list = None,
        system_prompt: str = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from Ollama"""
        try:
            url = f"{self.base_url}/api/generate"
            
            # Format conversation history
            context = ""
            if conversation_history:
                for msg in conversation_history:
                    context += f"{msg['role']}: {msg['content']}\n"
            
            prompt = f"{context}user: {message}\nassistant:"
            
            response = self.requests.post(
                url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
        
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            yield f"Error: {str(e)}"
    
    async def chat_sync(self, message: str, conversation_history: list = None) -> str:
        """Non-streaming response from Ollama"""
        try:
            url = f"{self.base_url}/api/generate"
            
            context = ""
            if conversation_history:
                for msg in conversation_history:
                    context += f"{msg['role']}: {msg['content']}\n"
            
            prompt = f"{context}user: {message}\nassistant:"
            
            response = self.requests.post(
                url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            import json
            data = response.json()
            return data.get("response", "No response")
        
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return f"Error: {str(e)}"


def get_provider(provider_name: str = None) -> AIProvider:
    """Factory function to get AI provider instance"""
    provider = provider_name or settings.default_provider
    
    providers = {
        "groq": GroqProvider,
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "ollama": OllamaProvider
    }
    
    provider_class = providers.get(provider.lower())
    if not provider_class:
        logger.warning(f"Provider {provider} not found, using Groq")
        provider_class = GroqProvider
    
    try:
        return provider_class()
    except Exception as e:
        logger.error(f"Failed to initialize {provider}: {e}")
        raise
