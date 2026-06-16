"""Voice processing for Aji OS - Speech recognition and text-to-speech"""

import logging
from typing import Optional
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

class VoiceProcessor:
    """Handle speech recognition and text-to-speech"""
    
    def __init__(self):
        """Initialize voice processor"""
        self.recognizer = None
        self.tts_engine = None
        self._init_speech_recognition()
        self._init_tts()
    
    def _init_speech_recognition(self) -> None:
        """Initialize speech recognition"""
        try:
            from speech_recognition import Recognizer
            self.recognizer = Recognizer()
            logger.info("Speech recognition initialized")
        except ImportError:
            logger.warning("SpeechRecognition not installed. Install with: pip install SpeechRecognition")
        except Exception as e:
            logger.error(f"Failed to initialize speech recognition: {e}")
    
    def _init_tts(self) -> None:
        """Initialize text-to-speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            logger.info("Text-to-speech engine initialized")
        except ImportError:
            logger.warning("pyttsx3 not installed. Install with: pip install pyttsx3")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
    
    async def recognize_speech(self, timeout: int = 5, language: str = "en-US") -> Optional[str]:
        """Recognize speech from microphone"""
        if not self.recognizer:
            logger.error("Speech recognizer not initialized")
            return None
        
        try:
            from speech_recognition import Microphone, UnknownValueError, RequestError
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            def _recognize():
                with Microphone() as source:
                    logger.info("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=timeout)
                    try:
                        text = self.recognizer.recognize_google(audio, language=language)
                        logger.info(f"Recognized: {text}")
                        return text
                    except UnknownValueError:
                        logger.warning("Could not understand audio")
                        return None
                    except RequestError as e:
                        logger.error(f"Google API error: {e}")
                        return None
            
            return await loop.run_in_executor(None, _recognize)
        
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    async def synthesize_speech(self, text: str, rate: int = 150) -> Optional[str]:
        """Convert text to speech"""
        if not self.tts_engine:
            logger.error("TTS engine not initialized")
            return None
        
        try:
            import pyttsx3
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            
            def _synthesize():
                output_file = Path("./data/tts_output.mp3")
                self.tts_engine.setProperty('rate', rate)
                self.tts_engine.save_to_file(text, str(output_file))
                self.tts_engine.runAndWait()
                logger.info(f"Synthesized speech saved to {output_file}")
                return str(output_file)
            
            return await loop.run_in_executor(None, _synthesize)
        
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return None
    
    def speak(self, text: str, rate: int = 150) -> None:
        """Speak text immediately (blocking)"""
        if not self.tts_engine:
            logger.error("TTS engine not initialized")
            return
        
        try:
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            logger.info(f"Spoke: {text}")
        except Exception as e:
            logger.error(f"Failed to speak: {e}")

# Global voice processor instance
voice_processor = VoiceProcessor()
