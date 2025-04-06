# LLM-based explanation generation
# backend/services/agent_explainer.py

from typing import Dict, Any


def generate_explanation(
    call_analysis: Dict[str, Any],
    dispatcher_report: Dict[str, Any],
    swat_check: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generates a natural language explanation for why a 911 call was flagged.

    Params:
        - call_analysis: Output from call_analysis module
        - dispatcher_report: Output from evaluate_dispatcher()
        - swat_check: Output from detect_swat()

    Returns:
        - A dictionary containing explanation text and structured flags
    """

    explanation_parts = []

    # Handle call analysis part
    urgency = call_analysis.get("urgency_score", 0.0)
    deception = call_analysis.get("deception_score", 0.0)

    if urgency > 0.85:
        explanation_parts.append("⚠️ High urgency detected in caller's statement.")
    if deception > 0.7:
        explanation_parts.append("⚠️ Possible deception detected in tone or content.")

    # SWAT flag check
    if swat_check.get("is_swat"):
        explanation_parts.append(f"🚨 SWAT risk: {swat_check.get('reason')}")

    # Dispatcher behavior check
    if dispatcher_report.get("neglect_flag"):
        explanation_parts.append("⚠️ Dispatcher flagged for high drop rate or neglect.")
    if dispatcher_report.get("fatigue_score", 0.0) > 0.6:
        explanation_parts.append("⚠️ Dispatcher may be experiencing fatigue.")
    if dispatcher_report.get("anomaly_detected"):
        explanation_parts.append("⚠️ Anomaly detected in dispatcher behavior pattern.")

    if not explanation_parts:
        explanation_parts.append("✅ No critical flags. Situation appears stable.")

    return {
        "summary": call_analysis.get("summary", "No summary available."),
        "explanation": " ".join(explanation_parts),
        "scores": {
            "urgency_score": round(urgency, 2),
            "deception_score": round(deception, 2),
            "fatigue_score": dispatcher_report.get("fatigue_score", 0.0),
            "neglect_flag": dispatcher_report.get("neglect_flag", False),
            "dispatcher_anomaly": dispatcher_report.get("anomaly_detected", False),
            "is_swat": swat_check.get("is_swat", False)
        }
    }
