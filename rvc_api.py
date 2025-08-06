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
        self.current_model_path = None
        self.current_index_path = None
        self.device = device if device else ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.performance_config = performance_config or {}
        
        # Performance settings
        self.batch_size = self.performance_config.get('batch_size', 1)
        self.max_memory_usage = self.performance_config.get('max_memory_mb', 4096)
        
        # Model cache for faster switching
        self.model_cache = {}
        self.cache_size_limit = self.performance_config.get('cache_size', 2)
        
        logger.info(f"RVC Converter initialized with device: {self.device}")
        logger.info(f"Performance config: batch_size={self.batch_size}, cache_size={self.cache_size_limit}")
        
        # Create temp directory for processing
        self.temp_dir = Path("storage/temp/rvc")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
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
            
            # Store model paths for later use
            self.current_model_path = model_path
            self.current_index_path = index_path
            self.current_model = model_name
            logger.info(f"Successfully prepared model: {model_name}")
            return True
                
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
        split_audio: bool = False,
        post_process: bool = False,
        **kwargs
    ) -> Optional[str]:
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
            split_audio: Whether to split long audio
            post_process: Whether to apply post-processing effects
            
        Returns:
            Output file path if successful, None otherwise
        """
        try:
            # Validate inputs
            if not os.path.exists(input_path):
                logger.error(f"Input file not found: {input_path}")
                return None
                
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Load model if not current
            if self.current_model != model_name:
                if not self.load_model(model_name):
                    logger.error(f"Failed to load model: {model_name}")
                    return None
            
            # Ensure voice converter is initialized
            if self.voice_converter is None:
                logger.error("Voice converter not initialized")
                return None
            
            # Perform voice conversion using stored model paths
            logger.info(f"Converting voice: {input_path} -> {output_path}")
            logger.info(f"Using model: {model_name} (pitch: {pitch}, index_rate: {index_rate})")
            
            self.voice_converter.convert_audio(
                audio_input_path=input_path,
                audio_output_path=output_path,
                model_path=self.current_model_path,
                index_path=self.current_index_path,
                pitch=pitch,
                f0_method=f0_method,
                index_rate=index_rate,
                volume_envelope=volume_envelope,
                protect=protect,
                hop_length=hop_length,
                clean_audio=clean_audio,
                clean_strength=clean_strength,
                split_audio=split_audio,
                post_process=post_process,
                **kwargs
            )
            
            # Verify output file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"Voice conversion completed: {output_path} ({file_size:,} bytes)")
                return output_path
            else:
                logger.error("Voice conversion failed - no output file generated")
                return None
                
        except Exception as e:
            logger.error(f"Error in voice conversion: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
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
            
            # Filter out training files (D_*.pth, G_*.pth) - keep only model files
            model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
            
            info = {
                "name": model_name,
                "path": str(model_dir),
                "pth_files": len(model_pth_files),
                "index_files": len(index_files),
                "has_pth": len(model_pth_files) > 0,
                "has_index": len(index_files) > 0,
                "status": "ready" if len(model_pth_files) > 0 else "incomplete",
                "all_pth_files": len(pth_files),  # Include training files count
                "model_files": [f.name for f in model_pth_files],
                "index_files_list": [f.name for f in index_files]
            }
            
            if model_pth_files:
                # Get file sizes
                pth_size = sum(f.stat().st_size for f in model_pth_files)
                info["pth_size_mb"] = round(pth_size / (1024 * 1024), 2)
                info["primary_model"] = model_pth_files[0].name
            
            if index_files:
                index_size = sum(f.stat().st_size for f in index_files)
                info["index_size_mb"] = round(index_size / (1024 * 1024), 2)
                info["primary_index"] = index_files[0].name
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting model info for {model_name}: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.voice_converter:
                del self.voice_converter
                self.voice_converter = None
            self.current_model = None
            
            # Clear model cache
            for model_name in list(self.model_cache.keys()):
                del self.model_cache[model_name]
            self.model_cache.clear()
            
            # Clean up temp files
            if hasattr(self, 'temp_dir') and self.temp_dir.exists():
                import shutil
                for temp_file in self.temp_dir.glob("*"):
                    try:
                        temp_file.unlink()
                    except:
                        pass
            
            # Free GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            logger.info("RVC Converter cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def convert_voice_batch(self, input_files: List[str], output_dir: str, 
                          model_name: str, **kwargs) -> List[str]:
        """
        Convert multiple audio files in batch for better efficiency
        
        Args:
            input_files: List of input file paths
            output_dir: Output directory
            model_name: RVC model name
            **kwargs: Additional parameters for conversion
            
        Returns:
            List of output file paths
        """
        try:
            # Load model once for batch
            if self.current_model != model_name:
                if not self.load_model(model_name):
                    logger.error(f"Failed to load model: {model_name}")
                    return []
            
            os.makedirs(output_dir, exist_ok=True)
            results = []
            
            for i, input_file in enumerate(input_files):
                if not os.path.exists(input_file):
                    logger.warning(f"Input file not found: {input_file}")
                    continue
                
                # Generate output filename
                input_name = Path(input_file).stem
                output_file = os.path.join(output_dir, f"{input_name}_rvc_{model_name}.wav")
                
                logger.info(f"Processing batch {i+1}/{len(input_files)}: {input_file}")
                
                result = self.convert_voice(
                    input_path=input_file,
                    output_path=output_file,
                    model_name=model_name,
                    **kwargs
                )
                
                if result:
                    results.append(result)
                    logger.info(f"Batch conversion {i+1} completed: {result}")
                else:
                    logger.warning(f"Batch conversion {i+1} failed: {input_file}")
            
            logger.info(f"Batch conversion completed: {len(results)}/{len(input_files)} successful")
            return results
            
        except Exception as e:
            logger.error(f"Error in batch conversion: {e}")
            return []
    
    def get_conversion_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get predefined conversion presets for different use cases"""
        return {
            "high_quality": {
                "pitch": 0,
                "index_rate": 0.85,
                "volume_envelope": 0.15,
                "protect": 0.4,
                "hop_length": 256,
                "f0_method": "rmvpe",
                "clean_audio": True,
                "clean_strength": 0.8,
                "split_audio": True,
                "post_process": True,
                "description": "Best quality, slower processing"
            },
            "fast": {
                "pitch": 0,
                "index_rate": 0.65,
                "volume_envelope": 0.3,
                "protect": 0.25,
                "hop_length": 512,
                "f0_method": "rmvpe",
                "clean_audio": False,
                "clean_strength": 0.5,
                "split_audio": False,
                "post_process": False,
                "description": "Fast processing, good quality"
            },
            "voice_clone": {
                "pitch": 0,
                "index_rate": 0.9,
                "volume_envelope": 0.1,
                "protect": 0.5,
                "hop_length": 128,
                "f0_method": "rmvpe",
                "clean_audio": True,
                "clean_strength": 0.9,
                "split_audio": True,
                "post_process": True,
                "description": "Maximum similarity to target voice"
            },
            "singing": {
                "pitch": 0,
                "index_rate": 0.7,
                "volume_envelope": 0.2,
                "protect": 0.2,
                "hop_length": 256,
                "f0_method": "crepe",
                "clean_audio": True,
                "clean_strength": 0.6,
                "split_audio": True,
                "post_process": True,
                "description": "Optimized for singing voice"
            }
        }


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