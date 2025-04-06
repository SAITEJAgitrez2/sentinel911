# Your local version
# backend/main.py

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List, Dict

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List, Dict


def compute_basic_stats(call_logs: List[Dict]) -> Dict:
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
            "total_calls": 0
        }

    avg_duration = df["duration"].mean()
    drop_rate = (df["status"] == "dropped").sum() / len(df)
    short_call_count = (df["duration"] < 10).sum()

    return {
        "avg_duration": round(avg_duration, 2),
        "drop_rate": round(drop_rate, 2),
        "short_call_count": int(short_call_count),
        "total_calls": len(df)
    }


def analyze_dispatcher_behavior(stats: Dict) -> Dict:
    """
    Analyzes dispatcher metrics and flags signs of fatigue or negligence.
    """
    fatigue_score = 0
    neglect_flag = False

    # Rule-based logic (can be upgraded to ML later)
    if stats["avg_duration"] > 30:
        fatigue_score += 0.4
    if stats["short_call_count"] > 5:
        fatigue_score += 0.3
    if stats["drop_rate"] > 0.25:
        fatigue_score += 0.3
        neglect_flag = True

    fatigue_score = round(min(fatigue_score, 1.0), 2)  # Clamp between 0 and 1

    return {
        "fatigue_score": fatigue_score,
        "neglect_flag": neglect_flag
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

    return anomaly_ratio > 0.25  # Threshold for flagging anomaly


def detect_anomaly_with_isolation_forest(call_logs: List[Dict]) -> bool:
    """
    Uses IsolationForest to detect anomalies in dispatcher behavior.
    Currently focuses on call durations as a time-series signal.

    Optional Enhancements (for future versions):
    - Include time gaps between calls to track idle spikes or overload
    - Integrate speech stress levels if voice/audio input is added
    - Add multi-feature anomaly detection (e.g., emotion tone, priority mismatch)
    """
    if len(call_logs) < 10:
        return False  # Not enough data to detect anomaly

    durations = [log["duration"] for log in call_logs]
    X = np.array(durations).reshape(-1, 1)

    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(X)

    preds = model.predict(X)  # -1 for anomaly, 1 for normal
    anomaly_ratio = (preds == -1).sum() / len(preds)

    return anomaly_ratio > 0.25  # Threshold for flagging anomaly



def evaluate_dispatcher(dispatcher_id: str, call_logs: List[Dict]) -> Dict:
    """
    Master function that processes dispatcher behavior and returns a full report.
    """
    stats = compute_basic_stats(call_logs)
    behavior_flags = analyze_dispatcher_behavior(stats)
    anomaly_flag = detect_anomaly_with_isolation_forest(call_logs)

    return {
        "dispatcher_id": dispatcher_id,
        "fatigue_score": behavior_flags["fatigue_score"],
        "neglect_flag": behavior_flags["neglect_flag"],
        "anomaly_detected": anomaly_flag,
        "details": stats
    }
