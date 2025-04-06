import json
from typing import Dict, Any
from typing import Optional
import json
import os

# Load known persons database from a JSON file
with open(os.path.join("../data/data", "known_persons.json"), "r") as f:
    KNOWN_PERSONS_DB = json.load(f)


# Load known individuals from a JSON file or hardcoded list
def load_known_individuals():
    try:
        with open("data/known_persons.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to default in-memory list if file not found
        return [
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

def detect_swat(call_text: str, caller_address: Optional[str] = None, caller_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Detects potential SWAT/prank calls based on mention of famous individuals or locations.

    Args:
        call_text (str): Transcript or summary of the call.
        caller_address (str): Optional reported address of the incident.

    Returns:
        Dict[str, Any]: Result with is_swat flag and reasoning.
    """
    call_text_lower = call_text.lower()

    for person in KNOWN_PERSONS_DB:
        person_address_lower = person['address'].lower()
        person_name_lower = person['name'].lower()

        if (
            person_name_lower in call_text_lower
            or (caller_address and person_address_lower in caller_address.lower())
            or person_address_lower in call_text_lower
        ):
            return {
                "is_swat": True,
                "person_flagged": person['name'],
                "famous_for": person['famous_for'],
                "reason": f"Call references {person['name']} ({person['famous_for']}) living at {person['address']}"
            }

    return {
        "is_swat": False,
        "reason": "No known individuals or flagged locations mentioned."
    }
