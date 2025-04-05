from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
from schemas.models import (
    CallAnalysisRequest, CallAnalysisResponse,
    DispatcherCheckRequest, DispatcherCheckResponse,
    SwatDetectionRequest, SwatDetectionResponse,
    TranscriptionRequest, TranscriptionResponse,
    AgentExplanationRequest, AgentExplanationResponse
)
from services import call_analysis, dispatcher, swat_detector, transcriber, agent

router = APIRouter()

@router.post("/analyze_call", response_model=CallAnalysisResponse)
async def analyze_call_endpoint(
    transcript: Optional[str] = None,
    audio_file: Optional[UploadFile] = File(None)
):
    """Analyze a 911 call transcript or audio file."""
    request = CallAnalysisRequest(transcript=transcript)
    return await call_analysis.analyze_call(request)

@router.post("/check_dispatcher", response_model=DispatcherCheckResponse)
async def check_dispatcher_endpoint(request: DispatcherCheckRequest):
    """Check dispatcher status and fatigue levels."""
    return await dispatcher.check_dispatcher(request)

@router.post("/detect_swat", response_model=SwatDetectionResponse)
async def detect_swat_endpoint(request: SwatDetectionRequest):
    """Detect potential SWATting attempts."""
    return await swat_detector.detect_swat(request)

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_endpoint(audio_file: UploadFile = File(...)):
    """Transcribe audio file to text."""
    request = TranscriptionRequest(audio_file=audio_file.filename)
    return await transcriber.transcribe_audio(request)

@router.get("/agent/explain", response_model=AgentExplanationResponse)
async def explain_endpoint(request: AgentExplanationRequest):
    """Get AI agent explanation of analysis."""
    return await agent.explain_analysis(request) 