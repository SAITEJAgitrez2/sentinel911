from pydantic import BaseModel
from typing import Optional, List

class CallAnalysisRequest(BaseModel):
    transcript: Optional[str] = None
    audio_file: Optional[str] = None

class CallAnalysisResponse(BaseModel):
    urgency_score: float
    deception_score: float
    summary: str

class DispatcherCheckRequest(BaseModel):
    dispatcher_id: int

class DispatcherCheckResponse(BaseModel):
    status: str  # normal/fatigued/flagged
    fatigue_score: float
    recent_calls: int

class SwatDetectionRequest(BaseModel):
    call_data: str
    dispatcher_id: int

class SwatDetectionResponse(BaseModel):
    is_swat: bool
    confidence: float
    reasoning: str

class TranscriptionRequest(BaseModel):
    audio_file: str

class TranscriptionResponse(BaseModel):
    transcript: str
    duration: float

class AgentExplanationRequest(BaseModel):
    analysis_data: dict

class AgentExplanationResponse(BaseModel):
    explanation: str
    confidence: float
    recommendations: List[str] 