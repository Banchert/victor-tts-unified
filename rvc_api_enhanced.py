#!/usr/bin/env python3
"""
🎭 Enhanced RVC API - ระบบ RVC ที่ปรับปรุงแล้ว
รวมฟีเจอร์ใหม่และการจัดการข้อผิดพลาดที่ดีขึ้น
"""

import os
import sys
import torch
import logging
import numpy as np
import traceback
import gc
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import threading
from concurrent.futures import ThreadPoolExecutor

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import RVC modules
try:
    from rvc.infer.infer import VoiceConverter
    RVC_AVAILABLE = True
except ImportError as e:
    logging.warning(f"RVC not available: {e}")
    RVC_AVAILABLE = False

logger = logging.getLogger("RVC_API_ENHANCED")

class EnhancedRVCConverter:
    """
    Enhanced RVC Voice Conversion API
    พร้อมฟีเจอร์ใหม่และการจัดการข้อผิดพลาดที่ดีขึ้น
    """
    
    def __init__(self, models_dir: str = "logs", device: str = None, 
                 performance_config: Dict[str, Any] = None):
        """
        Initialize Enhanced RVC Converter
        
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
        self.use_half_precision = self.performance_config.get('use_half_precision', True)
        
        # Model cache for faster switching
        self.model_cache = {}
        self.cache_size_limit = self.performance_config.get('cache_size', 2)
        
        # Thread safety
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # Status tracking
        self.is_initialized = False
        self.last_error = None
        self.conversion_stats = {
            'total_conversions': 0,
            'successful_conversions': 0,
            'failed_conversions': 0,
            'average_time': 0
        }
        
        logger.info(f"Enhanced RVC Converter initialized with device: {self.device}")
        logger.info(f"Performance config: batch_size={self.batch_size}, cache_size={self.cache_size_limit}")
        
        # Create temp directory for processing
        self.temp_dir = Path("storage/temp/rvc")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize if RVC is available
        if RVC_AVAILABLE:
            self._initialize_rvc()
        else:
            logger.error("RVC modules not available - voice conversion will be disabled")
    
    def _initialize_rvc(self):
        """Initialize RVC system"""
        try:
            with self._lock:
                if not self.is_initialized:
                    self.voice_converter = VoiceConverter()
                    self.is_initialized = True
                    logger.info("RVC system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RVC: {e}")
            self.last_error = str(e)
            self.is_initialized = False
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available RVC models with enhanced validation
        
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
            if model_name.startswith('.') or model_name in ['backups', 'imports']:
                continue
                
            pth_files = list(model_dir.glob("*.pth"))
            index_files = list(model_dir.glob("*.index"))
            
            # Filter out training files (D_*.pth, G_*.pth) - keep only model files
            model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
            
            # Enhanced validation
            if model_pth_files:
                model_info = {
                    'name': model_name,
                    'pth_files': [f.name for f in model_pth_files],
                    'index_files': [f.name for f in index_files],
                    'has_index': len(index_files) > 0,
                    'size_mb': sum(f.stat().st_size for f in model_pth_files) / (1024 * 1024)
                }
                
                if index_files:
                    logger.info(f"✅ Valid model found: {model_name} (pth: {len(model_pth_files)}, index: {len(index_files)})")
                else:
                    logger.warning(f"⚠️ Model {model_name} missing .index files - may work with reduced quality")
                
                models.append(model_name)
            else:
                logger.warning(f"❌ Model {model_name} missing .pth file")
        
        logger.info(f"Found {len(models)} valid RVC models: {models}")
        return models
    
    def load_model(self, model_name: str) -> bool:
        """
        Load RVC model with enhanced error handling
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            True if successful, False otherwise
        """
        if not RVC_AVAILABLE or not self.is_initialized:
            logger.error("RVC not available or not initialized")
            return False
        
        try:
            with self._lock:
                # Check if model is already loaded
                if self.current_model == model_name:
                    logger.info(f"Model {model_name} already loaded")
                    return True
                
                # Find model files
                model_dir = self.models_dir / model_name
                if not model_dir.exists():
                    logger.error(f"Model directory not found: {model_dir}")
                    return False
                
                pth_files = list(model_dir.glob("*.pth"))
                index_files = list(model_dir.glob("*.index"))
                
                # Filter model files
                model_pth_files = [f for f in pth_files if not (f.name.startswith('D_') or f.name.startswith('G_'))]
                
                if not model_pth_files:
                    logger.error(f"No valid .pth files found for model {model_name}")
                    return False
                
                model_path = str(model_pth_files[0])
                index_path = str(index_files[0]) if index_files else None
                
                # Load model using RVC
                logger.info(f"Loading model: {model_name}")
                logger.info(f"Model path: {model_path}")
                logger.info(f"Index path: {index_path}")
                
                # Cleanup previous model
                if self.voice_converter:
                    try:
                        self.voice_converter.cleanup_model()
                    except:
                        pass
                
                # Load new model
                self.voice_converter.load_model(model_path)
                
                # Update current model info
                self.current_model = model_name
                self.current_model_path = model_path
                self.current_index_path = index_path
                
                logger.info(f"✅ Model {model_name} loaded successfully")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to load model {model_name}: {e}")
            logger.error(traceback.format_exc())
            self.last_error = str(e)
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
        Convert voice with enhanced error handling and performance monitoring
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            model_name: Name of the RVC model to use
            pitch: Pitch shift (semitones)
            index_rate: Index rate for voice conversion
            volume_envelope: Volume envelope adjustment
            protect: Protection level for voice characteristics
            hop_length: Hop length for processing
            f0_method: F0 extraction method
            clean_audio: Whether to clean audio
            clean_strength: Audio cleaning strength
            split_audio: Whether to split audio for processing
            post_process: Whether to apply post-processing
            **kwargs: Additional parameters
            
        Returns:
            Path to output file if successful, None otherwise
        """
        if not RVC_AVAILABLE or not self.is_initialized:
            logger.error("RVC not available or not initialized")
            return None
        
        start_time = time.time()
        
        try:
            with self._lock:
                # Load model if needed
                if self.current_model != model_name:
                    if not self.load_model(model_name):
                        return None
                
                # Validate input file
                if not os.path.exists(input_path):
                    logger.error(f"Input file not found: {input_path}")
                    return None
                
                # Create output directory
                output_dir = Path(output_path).parent
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Convert audio
                logger.info(f"Converting voice: {input_path} -> {output_path}")
                logger.info(f"Parameters: pitch={pitch}, index_rate={index_rate}, f0_method={f0_method}")
                
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
                    split_audio=split_audio,
                    clean_audio=clean_audio,
                    post_process=post_process,
                    **kwargs
                )
                
                # Verify output
                if os.path.exists(output_path):
                    conversion_time = time.time() - start_time
                    self.conversion_stats['total_conversions'] += 1
                    self.conversion_stats['successful_conversions'] += 1
                    self.conversion_stats['average_time'] = (
                        (self.conversion_stats['average_time'] * (self.conversion_stats['successful_conversions'] - 1) + conversion_time) 
                        / self.conversion_stats['successful_conversions']
                    )
                    
                    logger.info(f"✅ Voice conversion completed in {conversion_time:.2f}s")
                    logger.info(f"Output: {output_path}")
                    return output_path
                else:
                    logger.error(f"❌ Output file not created: {output_path}")
                    self.conversion_stats['failed_conversions'] += 1
                    return None
                    
        except Exception as e:
            conversion_time = time.time() - start_time
            logger.error(f"❌ Voice conversion failed after {conversion_time:.2f}s: {e}")
            logger.error(traceback.format_exc())
            self.last_error = str(e)
            self.conversion_stats['failed_conversions'] += 1
            return None
    
    def is_available(self) -> bool:
        """Check if RVC is available and working"""
        return RVC_AVAILABLE and self.is_initialized
    
    def get_status(self) -> Dict[str, Any]:
        """Get detailed status information"""
        return {
            'available': self.is_available(),
            'initialized': self.is_initialized,
            'current_model': self.current_model,
            'device': self.device,
            'last_error': self.last_error,
            'conversion_stats': self.conversion_stats,
            'models_count': len(self.get_available_models()),
            'memory_usage_mb': self._get_memory_usage()
        }
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            if torch.cuda.is_available():
                return torch.cuda.memory_allocated() / (1024 * 1024)
            else:
                import psutil
                process = psutil.Process()
                return process.memory_info().rss / (1024 * 1024)
        except:
            return 0.0
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            with self._lock:
                if self.voice_converter:
                    self.voice_converter.cleanup_model()
                
                # Clear cache
                self.model_cache.clear()
                
                # Force garbage collection
                gc.collect()
                
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                logger.info("RVC resources cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_conversion_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get predefined conversion presets"""
        return {
            'natural': {
                'pitch': 0,
                'index_rate': 0.75,
                'volume_envelope': 0.25,
                'protect': 0.33,
                'f0_method': 'rmvpe',
                'clean_audio': True,
                'clean_strength': 0.7
            },
            'enhanced': {
                'pitch': 0,
                'index_rate': 0.85,
                'volume_envelope': 0.3,
                'protect': 0.25,
                'f0_method': 'rmvpe',
                'clean_audio': True,
                'clean_strength': 0.8
            },
            'aggressive': {
                'pitch': 0,
                'index_rate': 0.95,
                'volume_envelope': 0.4,
                'protect': 0.15,
                'f0_method': 'rmvpe',
                'clean_audio': True,
                'clean_strength': 0.9
            },
            'subtle': {
                'pitch': 0,
                'index_rate': 0.5,
                'volume_envelope': 0.15,
                'protect': 0.5,
                'f0_method': 'rmvpe',
                'clean_audio': False,
                'clean_strength': 0.3
            }
        }

# Global instance
_rvc_converter = None

def get_enhanced_rvc_converter(**kwargs) -> EnhancedRVCConverter:
    """Get or create global RVC converter instance"""
    global _rvc_converter
    if _rvc_converter is None:
        _rvc_converter = EnhancedRVCConverter(**kwargs)
    return _rvc_converter

def cleanup_enhanced_rvc():
    """Cleanup global RVC converter"""
    global _rvc_converter
    if _rvc_converter:
        _rvc_converter.cleanup()
        _rvc_converter = None 