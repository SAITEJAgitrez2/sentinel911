from schemas.models import SwatDetectionRequest, SwatDetectionResponse

async def detect_swat(request: SwatDetectionRequest) -> SwatDetectionResponse:
    """Mock SWAT detection service."""
    return SwatDetectionResponse(
        is_swat=False,
        confidence=0.95,
        reasoning="No suspicious patterns detected in call data. Standard emergency response appropriate."
    ) 