from fastapi import APIRouter, UploadFile, File, Form
from services.transcriber import transcribe_audio
from services.call_analysis import analyze_call


router = APIRouter()

@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    transcript = await transcribe_audio(file)
    return {"transcript": transcript}
@router.post("/analyze_call")
async def analyze_call_endpoint(transcript: str = Form(...)):
    result = analyze_call(transcript)
    return result
