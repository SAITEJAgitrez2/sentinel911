from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from services.transcriber import transcribe_audio
from services.call_analysis import analyze_call
from services.swat_detector import detect_swat
from backend.services.agent_explainer import generate_explanation
from backend.services.transcriber import transcribe_audio
from services.agent_explainer import generate_explanation
from services.dispatcher_monitor import evaluate_dispatcher
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter()

# --- Audio Transcription ---
@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    transcript = await transcribe_audio(file)
    return {"transcript": transcript}

# --- Call Analysis (Urgency, Deception, etc) ---
@router.post("/analyze_call")
async def analyze_call_endpoint(transcript: str = Form(...)):
    result = analyze_call(transcript)
    return result

# --- SWAT/Prank Detection ---
class CallInput(BaseModel):
    call_text: str
    caller_address: str
    caller_id: str = "Unknown"

class Call(BaseModel):
    transcript: str
    duration: Optional[float] = None
    status: Optional[str] = None
    timestamp: Optional[datetime] = None

class SessionRequest(BaseModel):
    dispatcher_id: str
    calls: List[Call]

@router.post("/detect_swat")
async def detect_swat_call(input: CallInput):
    try:
        result = detect_swat(input.call_text, input.caller_address, input.caller_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        

@router.post("/api/session_analysis")
async def session_analysis(payload: SessionRequest):
    dispatcher_id = payload.dispatcher_id
    calls = payload.calls

    call_logs = []

    for call in calls:
        result = analyze_call(
            transcript=call.transcript,
            duration=call.duration,
            status=call.status,
            timestamp=call.timestamp.isoformat() if call.timestamp else None
        )

        if "error" not in result:
            call_logs.append({
                "duration": result["duration"],
                "status": result["status"],
                "timestamp": result["timestamp"]
            })

    session_report = evaluate_dispatcher(dispatcher_id, call_logs)
    return session_report

class ExplainRequest(BaseModel):
    call_analysis: Dict[str, Any]
    dispatcher_report: Dict[str, Any]
    swat_check: Dict[str, Any]

@router.post("/agent/explain")
async def explain_agent_decision(payload: ExplainRequest):
    explanation = generate_explanation(
        payload.call_analysis,
        payload.dispatcher_report,
        payload.swat_check
    )
    return explanation
