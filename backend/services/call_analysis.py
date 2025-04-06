import tempfile
from datetime import datetime
from typing import Optional
import librosa
import whisper
from transformers import pipeline

# Load models
whisper_model = whisper.load_model("medium")
zero_shot_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
summary_model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

urgency_labels = ["high urgency", "low urgency", "not urgent"]
deception_labels = ["truthful", "deceptive"]

def analyze_call(
    audio_file: bytes,
    filename: Optional[str] = None,
    status: Optional[str] = None,
    timestamp: Optional[str] = None
) -> dict:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename or ".wav") as temp:
            temp.write(audio_file)
            audio_path = temp.name

        transcript_result = whisper_model.transcribe(audio_path)
        transcript = transcript_result["text"]

        try:
            y, sr = librosa.load(audio_path)
            duration = round(librosa.get_duration(y=y, sr=sr), 2)
        except Exception:
            duration = round(len(transcript.split()) / 3.0, 2)

        if not transcript or len(transcript.strip()) < 5:
            return {
                "urgency_score": 0.0,
                "deception_score": 0.0,
                "summary": "Transcript too short to analyze.",
                "duration": duration,
                "status": status or "completed",
                "timestamp": timestamp or datetime.utcnow().isoformat()
            }

        urgency_result = zero_shot_model(transcript, candidate_labels=urgency_labels)
        urgency_scores = dict(zip(urgency_result["labels"], urgency_result["scores"]))
        top_label, top_score = sorted(urgency_scores.items(), key=lambda x: x[1], reverse=True)[0]
        urgency_score = round(top_score if top_label == "high urgency" else 0.0, 2)

        deception_result = zero_shot_model(transcript, candidate_labels=deception_labels)
        deception_scores = dict(zip(deception_result["labels"], deception_result["scores"]))
        deception_score = round(deception_scores.get("deceptive", 0.0), 2)

        sentiment_result = sentiment_model(transcript)[0]
        sentiment = sentiment_result["label"]
        sentiment_score = sentiment_result["score"]

        if sentiment == "NEGATIVE" and sentiment_score > 0.7:
            deception_score = round(min(deception_score + 0.15, 1.0), 2)
        elif sentiment == "POSITIVE" and sentiment_score > 0.7:
            deception_score = round(max(deception_score - 0.1, 0.0), 2)

        summary_result = summary_model(
            transcript,
            max_length=10,
            min_length=5,
            do_sample=False
        )[0]["summary_text"]

        return {
            "urgency_score": urgency_score,
            "deception_score": deception_score,
            "summary": summary_result,
            "duration": duration,
            "status": status or "completed",
            "timestamp": timestamp or datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {"error": str(e)}
