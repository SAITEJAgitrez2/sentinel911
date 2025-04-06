# backend/services/dispatcher_monitor.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any


def compute_basic_stats(call_logs: List[Dict]) -> Dict[str, Any]:
    """
    Computes basic metrics from a list of dispatcher call logs.

    Each log should include: duration (in seconds), status, timestamp (ISO format).
    """
    df = pd.DataFrame(call_logs)

    if df.empty:
        return {
            "avg_duration": 0.0,
            "drop_rate": 0.0,
            "short_call_count": 0,
            "total_calls": 0,
            "instant_alert": False
        }

    avg_duration = float(df["duration"].mean())
    drop_rate = float((df["status"] == "dropped").sum() / len(df))
    short_call_count = int((df["duration"] < 1).sum())  # Calls less than 1 second
    instant_alert = bool(short_call_count > 0)  # 🚨 Raise alert if any instant call

    return {
        "avg_duration": avg_duration,
        "drop_rate": drop_rate,
        "short_call_count": short_call_count,
        "total_calls": int(len(df)),
        "instant_alert": instant_alert
    }


def analyze_dispatcher_behavior(stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes dispatcher metrics and flags signs of fatigue or negligence.
    """
    fatigue_score = 0.0
    neglect_flag = False

    # Rule-based logic (can be upgraded to ML later)
    if stats["avg_duration"] > 30:
        fatigue_score += 0.4
    if stats["short_call_count"] > 5:
        fatigue_score += 0.3
    if stats["drop_rate"] > 0.25:
        fatigue_score += 0.3
        neglect_flag = True

    fatigue_score = round(min(fatigue_score, 1.0), 2)

    return {
        "fatigue_score": fatigue_score,
        "neglect_flag": bool(neglect_flag)
    }


def detect_anomaly_with_isolation_forest(call_logs: List[Dict]) -> bool:
    """
    Uses IsolationForest to detect anomalies in dispatcher behavior.
    Focuses on call durations as a time-series signal.
    """
    if len(call_logs) < 10:
        return False  # Not enough data to detect anomaly

    durations = [log["duration"] for log in call_logs]
    X = np.array(durations).reshape(-1, 1)

    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(X)

    preds = model.predict(X)  # -1 for anomaly, 1 for normal
    anomaly_ratio = (preds == -1).sum() / len(preds)

    return bool(anomaly_ratio > 0.25)


def evaluate_dispatcher(dispatcher_id: str, call_logs: List[Dict]) -> Dict[str, Any]:
    """
    Master function that processes dispatcher behavior and returns a full report.
    """
    stats = compute_basic_stats(call_logs)
    behavior_flags = analyze_dispatcher_behavior(stats)
    anomaly_flag = detect_anomaly_with_isolation_forest(call_logs)

    return {
        "dispatcher_id": str(dispatcher_id),
        "fatigue_score": float(behavior_flags["fatigue_score"]),
        "neglect_flag": bool(behavior_flags["neglect_flag"]),
        "anomaly_detected": bool(anomaly_flag),
        "details": {
            "avg_duration": float(stats["avg_duration"]),
            "drop_rate": float(stats["drop_rate"]),
            "short_call_count": int(stats["short_call_count"]),
            "total_calls": int(stats["total_calls"]),
            "instant_alert": bool(stats["instant_alert"])
        }
    }
