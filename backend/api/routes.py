from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from services.transcriber import transcribe_audio
from services.call_analysis import analyze_call
from services.swat_detector import detect_swat

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

@router.post("/detect_swat")
async def detect_swat_call(input: CallInput):
    try:
        result = detect_swat(input.call_text, input.caller_address, input.caller_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
