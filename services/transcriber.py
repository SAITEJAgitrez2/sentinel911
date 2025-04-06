import tempfile
import whisper
from fastapi import UploadFile

# Load Whisper model once (choose model size based on accuracy/speed trade-off)
model = whisper.load_model("medium")  # You can also try "small", "medium", or "large"

async def transcribe_audio(file: UploadFile) -> str:
    try:
        # Save uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav" or ".mp3") as temp:
            contents = await file.read()
            temp.write(contents)
            temp_path = temp.name

        # Transcribe using Whisper
        result = model.transcribe(temp_path)
        return result["text"]

    except Exception as e:
        return f"Error during transcription: {str(e)}"
