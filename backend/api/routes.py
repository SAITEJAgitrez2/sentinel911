from fastapi import APIRouter, UploadFile, File
from services.transcriber import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    transcript = await transcribe_audio(file)
    return {"transcript": transcript}
