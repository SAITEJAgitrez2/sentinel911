from schemas.models import CallAnalysisRequest, CallAnalysisResponse

async def analyze_call(request: CallAnalysisRequest) -> CallAnalysisResponse:
    """Mock call analysis service."""
    return CallAnalysisResponse(
        urgency_score=0.85,
        deception_score=0.15,
        summary="Caller reported a vehicle accident with potential injuries. Dispatcher handled professionally."
    ) 