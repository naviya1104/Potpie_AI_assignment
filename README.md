Clarity – AI Decision Assistant

Clarity is a full-stack generative AI decision-making agent that helps users make better, structured decisions by analyzing context, constraints, and preferences.

It uses an AI agent built with PydanticAI, provides clear recommendations, reasoned explanations, confidence scores, and alternative options, all through a clean web interface.

🚀 Live Demo

(Add Netlify URL after deployment)

Frontend: https://your-netlify-link.netlify.app
Backend API: https://your-backend-url

🎯 Problem Statement

People often struggle to make decisions because:

Too many options

Unclear priorities

Conflicting constraints

Lack of structured reasoning

Clarity solves this by acting as an AI-powered decision assistant that:

Breaks down decisions logically

Explains why a recommendation is made

Provides confidence levels and alternatives

💡 Key Features
🔹 AI Decision Agent

Built using PydanticAI

Uses structured input/output schemas

Ensures predictable, validated AI responses

🔹 Structured Outputs

Each decision includes:

✅ One clear recommendation

🧠 Bullet-point reasoning

📊 Confidence score (0–1)

🔁 One alternative option

🔹 Robust Backend

FastAPI-based API

Timeout handling

Safe fallback responses

Detailed logging for observability

🔹 Clean Frontend UX

Simple, minimal UI

Loading states & error handling

Visual confidence indicator

Mobile responsive design

🏗️ Tech Stack
Frontend

HTML

CSS

Vanilla JavaScript

Hosted on Netlify

Backend

Python

FastAPI

Pydantic & PydanticAI

OpenRouter (LLM provider)

Hosted on Render / Railway🔄 API Flow (How It Works)

User enters decision details in the frontend

Frontend sends structured JSON to backend (/api/decision)

PydanticAI agent processes the request

LLM generates a response

Response is validated using Pydantic schemas

Structured output is returned to the UI

UI displays recommendation + reasoning + confidenc eEnvironment Variables

Create a .env file in backend/:

OPENAI_API_KEY=your_openrouter_api_key
MODEL_NAME=openai:gpt-4o-mini


⚠️ .env is ignored by git for security.
▶️ Run Locally
Backend
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload


Backend runs at:

http://localhost:8000


Swagger Docs:

http://localhost:8000/docs

Frontend

Open frontend/index.html

Or use Live Server in VS Code

🧪 Example Use Cases

Should I study DSA or ML first?

How should I prioritize my tasks today?

Should I buy or rent a laptop?

How to decide between multiple career options?

🛡️ Reliability & Safety

Timeout protection

Safe fallback responses

Input validation using Pydantic

Graceful error handling

Logging for debugging and monitoring

🌱 Future Improvements

User authentication

Decision history

Multi-agent decision collaboration

Personalized memory

Better UI animations

Mobile-first PWA
