from transformers import pipeline
from datetime import datetime

# Load HuggingFace pipelines
zero_shot_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)
summary_model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Labels for zero-shot classification
urgency_labels = ["high urgency", "low urgency", "not urgent"]
deception_labels = ["truthful", "deceptive"]


def analyze_call(
    transcript: str,
    duration: float = None,
    status: str = None,
    timestamp: str = None
) -> dict:
    try:
        if len(transcript.strip()) < 5:
            return {
                "urgency_score": 0.0,
                "deception_score": 0.0,
                "summary": "Transcript too short to analyze.",
                "duration": duration or 0.0,
                "status": status or "completed",
                "timestamp": timestamp or datetime.utcnow().isoformat()
            }

        # Zero-shot urgency detection
        urgency_result = zero_shot_model(transcript, candidate_labels=urgency_labels)
        urgency_scores = dict(zip(urgency_result["labels"], urgency_result["scores"]))
        sorted_urgency = sorted(urgency_scores.items(), key=lambda x: x[1], reverse=True)
        top_label, top_score = sorted_urgency[0]
        urgency_score = round(top_score if top_label == "high urgency" else 0.0, 2)

        # Zero-shot deception detection
        deception_result = zero_shot_model(transcript, candidate_labels=deception_labels)
        deception_scores = dict(zip(deception_result["labels"], deception_result["scores"]))
        deception_score = round(deception_scores.get("deceptive", 0.0), 2)

        # Sentiment adjustment
        sentiment_result = sentiment_model(transcript)[0]
        sentiment = sentiment_result["label"]
        sentiment_score = sentiment_result["score"]
        if sentiment == "NEGATIVE" and sentiment_score > 0.7:
            deception_score = round(min(deception_score + 0.15, 1.0), 2)
        elif sentiment == "POSITIVE" and sentiment_score > 0.7:
            deception_score = round(max(deception_score - 0.1, 0.0), 2)

        # Summarize the transcript
        summary_result = summary_model(
            transcript,
            max_length=50,
            min_length=15,
            do_sample=False
        )[0]["summary_text"]

        # Provide dispatcher-monitor-friendly metadata
        return {
            "urgency_score": urgency_score,
            "deception_score": deception_score,
            "summary": summary_result,
            "duration": duration or round(len(transcript.split()) / 3.0, 2),  # Approx duration in sec
            "status": status or "completed",
            "timestamp": timestamp or datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {"error": str(e)}
