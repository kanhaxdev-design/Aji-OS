"""Configuration management for Aji OS Backend"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    backend_host: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # AI Providers
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Default AI Configuration
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "groq")
    default_model: str = os.getenv("DEFAULT_MODEL", "mixtral-8x7b-32768")
    
    # AI Model Settings
    ai_temperature: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    ai_max_tokens: int = int(os.getenv("AI_MAX_TOKENS", "2048"))
    ai_system_prompt: str = os.getenv(
        "AI_SYSTEM_PROMPT",
        "You are Aji OS, a helpful and intelligent desktop assistant. Be concise and friendly."
    )
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/conversations.db")
    
    # Voice Configuration
    tts_engine: str = os.getenv("TTS_ENGINE", "pyttsx3")
    tts_voice_rate: int = int(os.getenv("TTS_VOICE_RATE", "150"))
    speech_recognition_language: str = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "en-US")
    speech_recognition_timeout: int = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "5"))
    
    # Features
    enable_voice: bool = os.getenv("ENABLE_VOICE", "true").lower() == "true"
    enable_plugins: bool = os.getenv("ENABLE_PLUGINS", "true").lower() == "true"
    enable_history: bool = os.getenv("ENABLE_HISTORY", "true").lower() == "true"
    enable_shortcuts: bool = os.getenv("ENABLE_SHORTCUTS", "true").lower() == "true"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/aji.log")
    
    # Security - CORS
    allowed_origins: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Ensure data directories exist
data_dir = Path("./data")
data_dir.mkdir(exist_ok=True)

log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

def setup_logging() -> logging.Logger:
    """Configure logging for the application"""
    
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("aji_os")
    logger.setLevel(settings.log_level)
    
    # File handler
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(settings.log_level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level)
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
