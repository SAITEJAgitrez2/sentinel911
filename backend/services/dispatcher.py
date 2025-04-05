from schemas.models import DispatcherCheckRequest, DispatcherCheckResponse

async def check_dispatcher(request: DispatcherCheckRequest) -> DispatcherCheckResponse:
    """Mock dispatcher check service."""
    return DispatcherCheckResponse(
        status="normal",
        fatigue_score=0.3,
        recent_calls=5
    ) 