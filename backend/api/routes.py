from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import traceback
from services.call_analysis import analyze_call
from services.swat_detector import detect_swat
from services.agent_explainer import generate_explanation
from services.dispatcher_monitor import evaluate_dispatcher

router = APIRouter()

# --- Call Analysis (Audio Only) ---
@router.post("/analyze_call", summary="Analyze call from audio file for urgency, deception, summary")
async def analyze_call_endpoint(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        result = analyze_call(audio_file=audio_bytes, filename=file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- SWAT/Prank Detection ---
class CallInput(BaseModel):
    call_text: str
    caller_address: str
    caller_id: str = "Unknown"

@router.post("/detect_swat")
async def detect_swat_call(input: CallInput):
    try:
        result = detect_swat(input.call_text, input.caller_address, input.caller_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Dispatcher Session Monitoring ---
class Call(BaseModel):
    transcript: str
    duration: Optional[float] = None
    status: Optional[str] = None
    timestamp: Optional[datetime] = None

class SessionRequest(BaseModel):
    dispatcher_id: str
    calls: List[Call]

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


# --- Agent Explanation ---
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


# --- Master Full Analysis ---
@router.post("/agent/full_analysis", summary="Complete analysis of a 911 call including SWAT, urgency, dispatcher, explanation")
async def full_analysis_endpoint(
    dispatcher_id: str = Form(...),
    caller_address: Optional[str] = Form(None),
    caller_id: Optional[str] = Form("Unknown"),
    file: UploadFile = File(...)
):
    try:
        # Transcribe + analyze the call
        audio_bytes = await file.read()
        call_analysis = analyze_call(audio_file=audio_bytes, filename=file.filename)

        if "error" in call_analysis:
            raise HTTPException(status_code=400, detail=call_analysis["error"])

        # Run SWAT check using summary + address
        swat_check = detect_swat(call_analysis["summary"], caller_address, caller_id)

        # Construct a simulated dispatcher session
        call_logs = [{
            "duration": call_analysis["duration"],
            "status": call_analysis["status"],
            "timestamp": call_analysis["timestamp"]
        }]
        dispatcher_report = evaluate_dispatcher(dispatcher_id, call_logs)

        # Combine all reports
        explanation = generate_explanation(
            call_analysis=call_analysis,
            dispatcher_report=dispatcher_report,
            swat_check=swat_check
        )

        return JSONResponse(content={
            "call_analysis": call_analysis,
            "swat_check": swat_check,
            "dispatcher_report": dispatcher_report,
            "explanation": explanation
        })

    except Exception as e:
        tb = traceback.format_exc()
        print("Error during full_analysis:", tb)
        return JSONResponse(
        status_code=500,
        content={
            "error": str(e),
            "traceback": tb
        }
    )
