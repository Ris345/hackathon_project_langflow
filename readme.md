
🏗️ System Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Langflow      │
│   (React/Vue)   │◄──►│  (FastAPI/Flask)│◄──►│   (LLM Chain)   │
│                 │    │                 │    │                 │
│ • User Input    │    │ • Job Scraping  │    │ • Question Gen  │
│ • Video Record  │    │ • Data Pipeline │    │ • Grading Logic │
│ • 3D Avatar     │    │ • API Gateway   │    │ • Tips Gen      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Digital Ocean │    │   Twelve Labs   │    │   External APIs │
│                 │    │                 │    │                 │
│ • App Hosting   │    │ • Video Analysis│    │ • Job Scraping  │
│ • Database      │    │ • Sentiment     │    │ • TTS/STT       │
│ • File Storage  │    │ • Body Language │    │ • 3D Avatar     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
🔧 Tech Stack
Frontend:

React/Vue.js for UI
WebRTC for video recording
Ready Player Me / VRM for 3D avatars
Web Speech API for voice interaction

Backend:

FastAPI (Python) for API
PostgreSQL for data storage
Redis for caching
Celery for background tasks

AI/ML:

Langflow for LLM orchestration
Twelve Labs for video analysis
OpenAI/Anthropic for LLM processing
ElevenLabs/Azure for TTS

Infrastructure:

Digital Ocean Droplets
Digital Ocean Spaces (S3-compatible storage)
Docker for containerization

📁 Project Structure
ai-interview-platform/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── Dockerfile
├── langflow/
│   ├── flows/
│   └── components/
├── docker-compose.yml
└── deploy/
    ├── nginx.conf
    └── docker-compose.prod.yml
