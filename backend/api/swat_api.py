from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.swat_detector import detect_swat

router = APIRouter()

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
