"""FastAPI main server for Aji OS"""

import logging
import uuid
from typing import Optional
from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import json

from config import settings, logger
from ai import ai_orchestrator
from memory import memory
from commands import command_router
from voice import voice_processor
from database import db
from plugins.system import SystemPlugin

# Initialize FastAPI app
app = FastAPI(
    title="Aji OS",
    description="AI Desktop Assistant Backend API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Pydantic Models
# ============================================

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_id: Optional[str] = None
    system_prompt: Optional[str] = None

class CommandRequest(BaseModel):
    """Command request model"""
    command: str
    args: Optional[dict] = None

class VoiceRequest(BaseModel):
    """Voice request model"""
    action: str  # "recognize" or "synthesize"
    text: Optional[str] = None

class ProviderSwitchRequest(BaseModel):
    """Provider switch request"""
    provider: str

class SettingsUpdate(BaseModel):
    """Settings update model"""
    key: str
    value: str

# ============================================
# Health & Info Endpoints
# ============================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Aji OS",
        "version": "1.0.0",
        "status": "running",
        "current_provider": ai_orchestrator.get_current_provider()
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_provider": ai_orchestrator.get_current_provider()
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return SystemPlugin.get_system_info()

# ============================================
# Chat Endpoints
# ============================================

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Stream chat response"""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Create conversation if needed
        conv_id = request.conversation_id
        if not conv_id:
            conv_id = memory.create_conversation()
        
        # Stream response
        async def response_generator():
            async for chunk in ai_orchestrator.chat(
                message=request.message,
                conversation_id=conv_id,
                system_prompt=request.system_prompt
            ):
                yield chunk
        
        return StreamingResponse(
            response_generator(),
            media_type="text/event-stream",
            headers={
                "X-Conversation-ID": conv_id,
                "Cache-Control": "no-cache"
            }
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat-sync")
async def chat_sync(request: ChatRequest):
    """Get complete chat response (non-streaming)"""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Create conversation if needed
        conv_id = request.conversation_id
        if not conv_id:
            conv_id = memory.create_conversation()
        
        # Get response
        response = await ai_orchestrator.chat_sync(
            message=request.message,
            conversation_id=conv_id
        )
        
        return {
            "conversation_id": conv_id,
            "response": response
        }
    
    except Exception as e:
        logger.error(f"Chat sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Conversation Management
# ============================================

@app.get("/api/conversations")
async def get_conversations(limit: int = 50):
    """Get conversation history"""
    try:
        conversations = db.get_conversations(limit)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get specific conversation"""
    try:
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete conversation"""
    try:
        success = db.delete_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear-history")
async def clear_history():
    """Clear all conversation history"""
    try:
        success = db.clear_all_conversations()
        if success:
            return {"message": "All conversations cleared"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear conversations")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Command Endpoints
# ============================================

@app.post("/api/command")
async def execute_command(request: CommandRequest):
    """Execute a system command through plugin system"""
    try:
        if not request.command.strip():
            raise HTTPException(status_code=400, detail="Command cannot be empty")
        
        result = await command_router.route_command(
            command=request.command,
            args=request.args or {}
        )
        return result
    
    except Exception as e:
        logger.error(f"Command execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/commands")
async def get_commands():
    """Get available commands"""
    try:
        commands = command_router.get_available_commands()
        return {"commands": commands}
    except Exception as e:
        logger.error(f"Error fetching commands: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/plugin/{plugin_name}")
async def get_plugin_info(plugin_name: str):
    """Get plugin information"""
    try:
        info = command_router.get_plugin_info(plugin_name)
        if "error" in info:
            raise HTTPException(status_code=404, detail=info["error"])
        return info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching plugin info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Voice Endpoints
# ============================================

@app.post("/api/voice/recognize")
async def recognize_speech(request: VoiceRequest):
    """Recognize speech from microphone"""
    try:
        if not settings.enable_voice:
            raise HTTPException(status_code=403, detail="Voice feature is disabled")
        
        text = await voice_processor.recognize_speech()
        if text:
            return {
                "status": "success",
                "text": text
            }
        else:
            return {
                "status": "error",
                "message": "Could not recognize speech"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Speech recognition error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice/synthesize")
async def synthesize_speech(request: VoiceRequest):
    """Convert text to speech"""
    try:
        if not settings.enable_voice:
            raise HTTPException(status_code=403, detail="Voice feature is disabled")
        
        if not request.text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        file_path = await voice_processor.synthesize_speech(request.text)
        if file_path:
            return {
                "status": "success",
                "file_path": file_path
            }
        else:
            return {
                "status": "error",
                "message": "Could not synthesize speech"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Speech synthesis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# Settings & Provider Endpoints
# ============================================

@app.post("/api/provider")
async def switch_provider(request: ProviderSwitchRequest):
    """Switch to different AI provider"""
    try:
        if request.provider not in ai_orchestrator.get_available_providers():
            raise HTTPException(
                status_code=400,
                detail=f"Provider {request.provider} not available"
            )
        
        success = ai_orchestrator.set_provider(request.provider)
        if success:
            return {
                "status": "success",
                "current_provider": ai_orchestrator.get_current_provider()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to switch provider")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Provider switch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/providers")
async def get_providers():
    """Get available AI providers"""
    return {
        "providers": ai_orchestrator.get_available_providers(),
        "current": ai_orchestrator.get_current_provider()
    }

@app.get("/api/settings")
async def get_settings():
    """Get current settings"""
    return {
        "provider": ai_orchestrator.get_current_provider(),
        "temperature": settings.ai_temperature,
        "max_tokens": settings.ai_max_tokens,
        "voice_enabled": settings.enable_voice,
        "plugins_enabled": settings.enable_plugins
    }

@app.post("/api/settings")
async def update_setting(request: SettingsUpdate):
    """Update a setting"""
    try:
        success = db.set_setting(request.key, request.value)
        if success:
            return {
                "status": "success",
                "message": f"Setting {request.key} updated"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update setting")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Settings update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# WebSocket for Real-time Chat
# ============================================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    conversation_id = memory.create_conversation()
    
    try:
        while True:
            data = await websocket.receive_text()
            request_data = json.loads(data)
            
            message = request_data.get("message")
            if not message:
                await websocket.send_json({
                    "type": "error",
                    "message": "Message is required"
                })
                continue
            
            # Send typing indicator
            await websocket.send_json({
                "type": "typing",
                "conversation_id": conversation_id
            })
            
            # Stream response
            response_text = ""
            try:
                async for chunk in ai_orchestrator.chat(
                    message=message,
                    conversation_id=conversation_id
                ):
                    response_text += chunk
                    await websocket.send_json({
                        "type": "message",
                        "chunk": chunk,
                        "conversation_id": conversation_id
                    })
                
                # Send complete message
                await websocket.send_json({
                    "type": "complete",
                    "message": response_text,
                    "conversation_id": conversation_id
                })
            
            except Exception as e:
                logger.error(f"WebSocket chat error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting Aji OS Backend on {settings.backend_host}:{settings.backend_port}")
    logger.info(f"AI Provider: {settings.default_provider}")
    logger.info(f"Frontend URL: {settings.frontend_url}")
    
    uvicorn.run(
        app,
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
