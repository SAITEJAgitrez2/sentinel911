from schemas.models import TranscriptionRequest, TranscriptionResponse

async def transcribe_audio(request: TranscriptionRequest) -> TranscriptionResponse:
    """Mock transcription service."""
    return TranscriptionResponse(
        transcript="911, what's your emergency? There's been a car accident on Main Street. Are there any injuries? Yes, one person is trapped in their vehicle.",
        duration=45.5
    ) 