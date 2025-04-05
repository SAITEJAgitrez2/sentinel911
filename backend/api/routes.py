from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from models.database import Call, Dispatcher, Alert
from services.ml_service import MLService
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter()
ml_service = MLService()

@router.post("/calls/analyze")
async def analyze_call(
    audio_file: UploadFile = File(...),
    dispatcher_id: int = None,
    db: Session = Depends(get_db)
):
    """Analyze a new 911 call."""
    try:
        # Save audio file
        audio_path = f"data/audio/{audio_file.filename}"
        with open(audio_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Transcribe audio
        transcript = await ml_service.transcribe_audio(audio_path)
        
        # Analyze call
        urgency_score = await ml_service.analyze_urgency(transcript)
        deception_score = await ml_service.detect_deception(transcript)
        
        # Create call record
        call = Call(
            transcript=transcript,
            audio_path=audio_path,
            urgency_score=urgency_score,
            deception_score=deception_score,
            dispatcher_id=dispatcher_id
        )
        db.add(call)
        db.commit()
        
        return {
            "call_id": call.id,
            "transcript": transcript,
            "urgency_score": urgency_score,
            "deception_score": deception_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calls/{call_id}")
async def get_call(call_id: int, db: Session = Depends(get_db)):
    """Get call details by ID."""
    call = db.query(Call).filter(Call.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.get("/alerts")
async def get_alerts(
    resolved: bool = None,
    db: Session = Depends(get_db)
):
    """Get all alerts with optional filter."""
    query = db.query(Alert)
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    return query.all()

@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Mark an alert as resolved."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_resolved = True
    db.commit()
    return {"status": "success"} 