"""Database operations for Aji OS"""

import json
from datetime import datetime
from typing import List, Optional, Dict, Any
import sqlite3
from pathlib import Path

class Database:
    """SQLite database handler for conversations and history"""
    
    def __init__(self, db_path: str = "./data/conversations.db"):
        """Initialize database connection"""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                provider TEXT,
                model TEXT
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        
        # Settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_conversation(self, conv_id: str, title: str, provider: str, model: str) -> bool:
        """Create a new conversation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversations (id, title, provider, model)
                VALUES (?, ?, ?, ?)
            """, (conv_id, title, provider, model))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return False
    
    def add_message(
        self,
        msg_id: str,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Add a message to a conversation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            metadata_str = json.dumps(metadata) if metadata else None
            cursor.execute("""
                INSERT INTO messages (id, conversation_id, role, content, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (msg_id, conversation_id, role, content, metadata_str))
            
            # Update conversation timestamp
            cursor.execute("""
                UPDATE conversations SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation and its messages"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get conversation
            cursor.execute("""
                SELECT * FROM conversations WHERE id = ?
            """, (conversation_id,))
            conv = cursor.fetchone()
            
            if not conv:
                return None
            
            # Get messages
            cursor.execute("""
                SELECT * FROM messages WHERE conversation_id = ?
                ORDER BY timestamp ASC
            """, (conversation_id,))
            messages = cursor.fetchall()
            
            conn.close()
            
            return {
                "id": conv["id"],
                "title": conv["title"],
                "created_at": conv["created_at"],
                "updated_at": conv["updated_at"],
                "provider": conv["provider"],
                "model": conv["model"],
                "messages": [
                    {
                        "id": msg["id"],
                        "role": msg["role"],
                        "content": msg["content"],
                        "timestamp": msg["timestamp"],
                        "metadata": json.loads(msg["metadata"]) if msg["metadata"] else None
                    }
                    for msg in messages
                ]
            }
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
    
    def get_conversations(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all conversations, ordered by most recent"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conversations
                ORDER BY updated_at DESC
                LIMIT ?
            """, (limit,))
            
            conversations = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": conv["id"],
                    "title": conv["title"],
                    "created_at": conv["created_at"],
                    "updated_at": conv["updated_at"],
                    "provider": conv["provider"],
                    "model": conv["model"]
                }
                for conv in conversations
            ]
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation and its messages"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM messages WHERE conversation_id = ?
            """, (conversation_id,))
            cursor.execute("""
                DELETE FROM conversations WHERE id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    def clear_all_conversations(self) -> bool:
        """Clear all conversations and messages"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages")
            cursor.execute("DELETE FROM conversations")
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing conversations: {e}")
            return False
    
    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            """, (key, value))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error setting value: {e}")
            return False
    
    def get_setting(self, key: str, default: str = "") -> str:
        """Get a setting value"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else default
        except Exception as e:
            print(f"Error getting setting: {e}")
            return default

# Global database instance
db = Database()
