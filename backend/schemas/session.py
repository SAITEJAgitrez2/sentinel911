# backend/schemas/session.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CallInput(BaseModel):
    transcript: str
    duration: Optional[float] = None
    status: Optional[str] = "completed"
    timestamp: Optional[datetime] = None

class SessionRequest(BaseModel):
    dispatcher_id: str
    calls: List[CallInput]
