"""Conversation memory management for Aji OS"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class ConversationMemory:
    """Manage conversation history and context"""
    
    def __init__(self, max_memory: int = 10):
        """Initialize conversation memory
        
        Args:
            max_memory: Maximum number of previous messages to keep in context
        """
        self.max_memory = max_memory
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.current_conversation_id: Optional[str] = None
    
    def create_conversation(self) -> str:
        """Create a new conversation"""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = []
        self.current_conversation_id = conv_id
        logger.info(f"Created conversation: {conv_id}")
        return conv_id
    
    def add_message(
        self,
        role: str,
        content: str,
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add message to conversation"""
        conv_id = conversation_id or self.current_conversation_id
        
        if not conv_id or conv_id not in self.conversations:
            conv_id = self.create_conversation()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[conv_id].append(message)
        logger.debug(f"Added {role} message to {conv_id}")
    
    def get_context(
        self,
        conversation_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation context (for AI prompt)"""
        conv_id = conversation_id or self.current_conversation_id
        
        if not conv_id or conv_id not in self.conversations:
            return []
        
        messages = self.conversations[conv_id]
        limit = limit or self.max_memory
        
        # Return last N messages, formatted for AI
        context_messages = messages[-limit:]
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in context_messages
        ]
    
    def get_full_conversation(self, conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get complete conversation history"""
        conv_id = conversation_id or self.current_conversation_id
        
        if not conv_id or conv_id not in self.conversations:
            return []
        
        return self.conversations[conv_id]
    
    def clear_current_conversation(self) -> None:
        """Clear current conversation"""
        if self.current_conversation_id:
            self.conversations[self.current_conversation_id] = []
            logger.info(f"Cleared conversation: {self.current_conversation_id}")
    
    def delete_conversation(self, conversation_id: str) -> None:
        """Delete a conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
            logger.info(f"Deleted conversation: {conversation_id}")
    
    def switch_conversation(self, conversation_id: str) -> bool:
        """Switch to a different conversation"""
        if conversation_id in self.conversations:
            self.current_conversation_id = conversation_id
            logger.info(f"Switched to conversation: {conversation_id}")
            return True
        return False
    
    def get_all_conversations(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all conversations"""
        return self.conversations
    
    def get_conversation_summary(self, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Get conversation metadata and summary"""
        conv_id = conversation_id or self.current_conversation_id
        
        if not conv_id or conv_id not in self.conversations:
            return {}
        
        messages = self.conversations[conv_id]
        
        return {
            "id": conv_id,
            "message_count": len(messages),
            "created_at": messages[0]["timestamp"] if messages else None,
            "last_updated": messages[-1]["timestamp"] if messages else None,
            "preview": messages[0]["content"][:100] if messages else ""
        }

# Global memory instance
memory = ConversationMemory()
