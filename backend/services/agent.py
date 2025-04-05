from schemas.models import AgentExplanationRequest, AgentExplanationResponse

async def explain_analysis(request: AgentExplanationRequest) -> AgentExplanationResponse:
    """Mock agent explanation service."""
    return AgentExplanationResponse(
        explanation="Based on the call analysis, this appears to be a legitimate emergency requiring immediate response. The caller's tone and description indicate high urgency.",
        confidence=0.92,
        recommendations=[
            "Dispatch emergency services immediately",
            "Monitor dispatcher fatigue levels",
            "Document all response times"
        ]
    ) 