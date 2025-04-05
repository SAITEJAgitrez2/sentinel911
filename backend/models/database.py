from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(Text)
    audio_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)
    urgency_score = Column(Float)
    deception_score = Column(Float)
    anomaly_score = Column(Float)
    dispatcher_id = Column(Integer, ForeignKey("dispatchers.id"))
    
    dispatcher = relationship("Dispatcher", back_populates="calls")
    alerts = relationship("Alert", back_populates="call")

class Dispatcher(Base):
    __tablename__ = "dispatchers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    badge_number = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    
    calls = relationship("Call", back_populates="dispatcher")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.id"))
    alert_type = Column(String)  # urgency, deception, anomaly
    severity = Column(Float)
    explanation = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)
    
    call = relationship("Call", back_populates="alerts") 