import os

# Define the enhanced Sentinel911 project structure
structure = {
    "backend": {
        "api": {
            "__init__.py": "",
            "routes.py": "# FastAPI route definitions"
        },
        "schemas": {
            "__init__.py": "",
            "models.py": "# Pydantic models for request/response"
        },
        "services": {
            "__init__.py": "",
            "call_analysis.py": "# NLP classifier logic",
            "dispatcher_monitor.py": "# Anomaly detection logic",
            "swat_detector.py": "# SWAT call detection logic",
            "agent_explainer.py": "# LLM-based explanation generation"
        },
        "utils": {
            "__init__.py": "",
            "helpers.py": "# Shared utility functions"
        },
        "config.py": "# Environment config, constants, paths"
    },
    "frontend": {
        "src": {
            "components": {
                "CallInput.tsx": "// React component for input form",
                "ResultCard.tsx": "// Displays individual result blocks"
            },
            "hooks": {
                "useApi.ts": "// Custom hook to handle API calls"
            }
        }
    },
    "data": {
        "transcripts": {},
        "sample_audio": {},
        "dispatcher_logs.csv": "# Sample call log data",
        "verified_users.csv": "# Sample verified user list"
    },
    "notebooks": {
        "nlp_model_training.ipynb": "",
        "anomaly_detection_exploration.ipynb": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)

# Run this in the project root (e.g., inside `sentinel911/`)
if __name__ == "__main__":
    create_structure(".", structure)
