from transformers import pipeline
import torch
from typing import Dict, List, Tuple
import numpy as np
from core.config import settings
import whisper
import pyod.models.iforest

class MLService:
    def __init__(self):
        # Initialize NLP models
        self.urgency_classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        
        self.deception_detector = pipeline(
            "text-classification",
            model="distilbert-base-uncased",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Initialize Whisper for speech-to-text
        self.whisper_model = whisper.load_model(settings.WHISPER_MODEL)
        
        # Initialize anomaly detection
        self.anomaly_detector = pyod.models.iforest.IForest(
            contamination=0.1,
            random_state=42
        )
        
    async def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file to text using Whisper."""
        result = self.whisper_model.transcribe(audio_path)
        return result["text"]
    
    async def analyze_urgency(self, text: str) -> float:
        """Analyze text for urgency level."""
        result = self.urgency_classifier(text)
        return float(result[0]["score"])
    
    async def detect_deception(self, text: str) -> float:
        """Detect potential deception in text."""
        result = self.deception_detector(text)
        return float(result[0]["score"])
    
    async def detect_anomalies(self, features: np.ndarray) -> Tuple[float, bool]:
        """Detect anomalies in dispatcher behavior features."""
        score = self.anomaly_detector.decision_function([features])[0]
        is_anomaly = score > settings.ANOMALY_DETECTION_THRESHOLD
        return float(score), is_anomaly
    
    async def explain_alert(self, alert_type: str, data: Dict) -> str:
        """Generate explanation for alerts using LangChain."""
        # TODO: Implement LangChain-based explanation generation
        return f"Alert of type {alert_type} detected with confidence {data.get('score', 0)}" 