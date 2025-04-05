# Sentinel911 🚨

An AI-powered emergency oversight system for 911 call centers that uses NLP, anomaly detection, and agentic AI to analyze call transcripts and dispatcher behavior.

## 🚀 Features

- Real-time call transcript analysis using NLP
- Anomaly detection for dispatcher behavior patterns
- Agentic AI system for alert explanation and reasoning
- Modern React dashboard for monitoring and analysis
- FastAPI backend with clean architecture
- ML/LLM models for processing and reasoning

## 🏗️ Project Structure

```
.
├── backend/           # FastAPI application
├── frontend/         # React (Vite) dashboard
├── data/            # Sample data and logs
├── notebooks/       # Development and experimentation
└── docs/           # Documentation
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, PyOD, HuggingFace Transformers, SHAP, LangChain
- **Frontend**: React, TailwindCSS, Vite
- **ML**: NLP (urgency/deception), Anomaly Detection, Whisper (STT)
- **Agent**: LangChain with explainability

## 🚦 Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   ```
4. Start the development servers:
   ```bash
   # Backend
   cd backend
   uvicorn main:app --reload

   # Frontend
   cd frontend
   npm run dev
   ```

## 🐳 Docker

Run the entire stack with:
```bash
docker-compose up
```

" Testing" 
