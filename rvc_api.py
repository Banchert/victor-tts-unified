"""
RVC API Wrapper - Voice Conversion System
Enhanced implementation for RVC voice cloning
"""

import os
import sys
import torch
import logging
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import RVC modules
from rvc.infer.infer import VoiceConverter

logger = logging.getLogger("RVC_API")

class RVCConverter:
    """
    Advanced RVC Voice Conversion API
    Supports multiple models, voice effects, and high-quality audio processing
    """
    
    def __init__(self, models_dir: str = "logs", device: str = None, performance_config: Dict[str, Any] = None):
        """
        Initialize RVC Converter
        
        Args:
            models_dir: Directory containing RVC models
            device: Device to use (cuda:0, cpu, etc.)
            performance_config: Performance configuration dict
        """
        self.models_dir = Path(models_dir)
        self.voice_converter = None
        self.current_model = None
        self.device = device if device else ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.performance_config = performance_config or {}
        
        logger.info(f"RVC Converter initialized with device: {self.device}")
        
    def get_available_models(self) -> List[str]:
        """
        Get list of available RVC models
        
        Returns:
            List of model names
        """
        models = []
        
        if not self.models_dir.exists():
            logger.warning(f"Models directory not found: {self.models_dir}")
            return models
            
        for model_dir in self.models_dir.iterdir():
            if not model_dir.is_dir():
                continue
                
            model_name = model_dir.name
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            # Filter out training files (D_*.pth, G_*.pth) - keep only model files
            model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
            
            # Check if model has required files
            if model_pth_files:
                if index_files:
                    logger.info(f"Valid model found: {model_name} (pth: {len(model_pth_files)}, index: {len(index_files)})")
                    models.append(model_name)
                else:
                    logger.warning(f"Model {model_name} missing .index files")
                    # Still add it - some models might work without index
                    models.append(model_name)
            else:
                logger.warning(f"Model {model_name} missing .pth file")
        
        logger.info(f"Found {len(models)} valid RVC models: {models}")
        return models
    
    def load_model(self, model_name: str) -> bool:
        """
        Load specific RVC model
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            True if successful, False otherwise
        """
        try:
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                logger.error(f"Model directory not found: {model_dir}")
                return False
            
            # Find model files
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            # Filter out training files (D_*.pth, G_*.pth) - keep only model files
            model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
            
            if not model_pth_files:
                logger.error(f"No model .pth files found for model: {model_name}")
                return False
            
            # Use the first model .pth file found
            model_path = str(model_pth_files[0])
            index_path = str(index_files[0]) if index_files else None
            
            logger.info(f"Loading model: {model_path}")
            if index_path:
                logger.info(f"Using index: {index_path}")
            
            # Initialize voice converter if not already done
            if self.voice_converter is None:
                self.voice_converter = VoiceConverter()
            
            # Load the model
            success = self.voice_converter.load_model(
                model_path=model_path,
                index_path=index_path,
                device=self.device
            )
            
            if success:
                self.current_model = model_name
                logger.info(f"Successfully loaded model: {model_name}")
                return True
            else:
                logger.error(f"Failed to load model: {model_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            return False
    
    def convert_voice(
        self,
        input_path: str,
        output_path: str,
        model_name: str,
        pitch: int = 0,
        index_rate: float = 0.75,
        volume_envelope: float = 0.25,
        protect: float = 0.33,
        hop_length: int = 512,
        f0_method: str = "rmvpe",
        clean_audio: bool = True,
        clean_strength: float = 0.7,
        **kwargs
    ) -> bool:
        """
        Convert voice using RVC
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            model_name: Name of RVC model to use
            pitch: Pitch adjustment (-12 to +12 semitones)
            index_rate: Index rate (0.0 to 1.0)
            volume_envelope: Volume envelope (0.0 to 1.0)
            protect: Protect consonants (0.0 to 0.5)
            hop_length: Hop length for processing
            f0_method: F0 extraction method (rmvpe, crepe, fcpe)
            clean_audio: Whether to clean audio
            clean_strength: Audio cleaning strength
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Load model if not current
            if self.current_model != model_name:
                if not self.load_model(model_name):
                    return False
            
            # Ensure voice converter is initialized
            if self.voice_converter is None:
                logger.error("Voice converter not initialized")
                return False
            
            # Perform voice conversion
            success = self.voice_converter.convert_audio(
                input_path=input_path,
                output_path=output_path,
                pitch=pitch,
                index_rate=index_rate,
                volume_envelope=volume_envelope,
                protect=protect,
                hop_length=hop_length,
                f0_method=f0_method,
                clean_audio=clean_audio,
                clean_strength=clean_strength
            )
            
            if success and os.path.exists(output_path):
                logger.info(f"Voice conversion completed: {input_path} -> {output_path}")
                return True
            else:
                logger.error("Voice conversion failed - no output file generated")
                return False
                
        except Exception as e:
            logger.error(f"Error in voice conversion: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if RVC system is available
        
        Returns:
            True if RVC is available and working
        """
        try:
            models = self.get_available_models()
            return len(models) > 0
        except Exception as e:
            logger.error(f"Error checking RVC availability: {e}")
            return False
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary with model information
        """
        try:
            model_dir = self.models_dir / model_name
            if not model_dir.exists():
                return {"error": "Model not found"}
            
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            info = {
                "name": model_name,
                "path": str(model_dir),
                "pth_files": len(pth_files),
                "index_files": len(index_files),
                "has_pth": len(pth_files) > 0,
                "has_index": len(index_files) > 0,
                "status": "ready" if len(pth_files) > 0 else "incomplete"
            }
            
            if pth_files:
                # Get file sizes
                pth_size = sum(f.stat().st_size for f in pth_files)
                info["pth_size_mb"] = round(pth_size / (1024 * 1024), 2)
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.voice_converter:
                del self.voice_converter
                self.voice_converter = None
            self.current_model = None
            logger.info("RVC Converter cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


# Global instance for easy access
rvc_converter = None

def get_rvc_converter() -> RVCConverter:
    """Get global RVC converter instance"""
    global rvc_converter
    if rvc_converter is None:
        rvc_converter = RVCConverter()
    return rvc_converter


if __name__ == "__main__":
    # Test the RVC converter
    converter = RVCConverter()
    
    print("🔍 Testing RVC Converter...")
    print(f"Device: {converter.device}")
    
    models = converter.get_available_models()
    print(f"Available models: {len(models)}")
    
    for model in models[:3]:  # Show first 3 models
        info = converter.get_model_info(model)
        print(f"Model: {model} - Status: {info.get('status', 'unknown')}")
    
    print(f"RVC Available: {converter.is_available()}") 