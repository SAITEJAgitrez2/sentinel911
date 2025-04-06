# SWAT call detection logic
import json
from typing import Dict, Any

# Sample database of known individuals (this can be replaced with a DB or external API)
KNOWN_PERSONS_DB = [
    {
        "name": "John Doe",
        "address": "123 Hollywood Blvd",
        "famous_for": "Actor - Starred in 'Action Hero 3'"
    },
    {
        "name": "Jane Smith",
        "address": "456 Music Lane",
        "famous_for": "Grammy-winning Musician"
    },
    {
        "name": "Ali Khan",
        "address": "789 Streamer Street",
        "famous_for": "Popular Twitch Streamer"
    }
]

def detect_swat(call_text: str, caller_address: str) -> Dict[str, Any]:
    """
    Detects potential SWAT/prank calls based on mention of famous individuals.

    Args:
        call_text (str): Transcription of the emergency call.
        caller_address (str): The reported address of the incident.

    Returns:
        Dict[str, Any]: Result with is_swat flag and reasoning.
    """
    call_text_lower = call_text.lower()
    for person in KNOWN_PERSONS_DB:
        if person['name'].lower() in call_text_lower or person['address'].lower() in caller_address.lower():
            return {
                "is_swat": True,
                "person_flagged": person['name'],
                "famous_for": person['famous_for'],
                "reason": f"Call references {person['name']} ({person['famous_for']}) living at {person['address']}"
            }
    
    return {
        "is_swat": False,
        "reason": "No mention of known individuals detected."
    }
