# 🧠 Clarity – AI Decision Assistant

Clarity is a full-stack generative AI decision-making agent that helps users make better, structured decisions by analyzing context, constraints, and preferences.

It uses an AI agent built with **PydanticAI** and provides clear recommendations, reasoned explanations, confidence scores, and alternative options through a clean web interface.

---

## 🚀 Live Demo

Frontend: https://your-netlify-link.netlify.app  
Backend API: https://your-backend-url

---

## 🎯 Problem Statement

People often struggle to make decisions because:
- Too many options
- Unclear priorities
- Conflicting constraints
- Lack of structured reasoning

Clarity solves this by acting as an AI-powered decision assistant that:
- Breaks down decisions logically
- Explains *why* a recommendation is made
- Provides confidence levels and alternatives

---

## 💡 Key Features

### AI Decision Agent
- Built using **PydanticAI**
- Structured input and output schemas
- Predictable, validated AI responses

### Structured Outputs
Each decision includes:
- One clear recommendation
- Bullet-point reasoning
- Confidence score (0–1)
- One alternative option

### Robust Backend
- FastAPI-based API
- Timeout handling
- Safe fallback responses
- Detailed logging

### Clean Frontend UX
- Simple and minimal UI
- Loading and error states
- Visual confidence indicator
- Responsive design

---

## 🏗️ Tech Stack

**Frontend**
- HTML
- CSS
- JavaScript
- Netlify

**Backend**
- Python
- FastAPI
- Pydantic & PydanticAI
- OpenRouter (LLM provider)

---


---

## 🔄 How It Works

1. User enters decision details in the frontend
2. Frontend sends structured JSON to the backend
3. PydanticAI agent processes the request
4. LLM generates a response
5. Output is validated using Pydantic schemas
6. Structured response is returned to the UI

---

## 🔐 Environment Variables

Create a `.env` file inside `backend/`:
OPENAI_API_KEY=your_openrouter_api_key
MODEL_NAME=openai:gpt-4o-mini


> The `.env` file is ignored by git for security.

---

## ▶️ Run Locally

### Backend
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload


Backend URL:
http://localhost:8000


Swagger Docs:
http://localhost:8000/docs


---

### Frontend

Open `frontend/index.html`  
or use VS Code Live Server.

---

## 🧪 Example Use Cases

- Should I study DSA or ML first?
- How should I prioritize my tasks today?
- Should I buy or rent a laptop?
- How to choose between multiple career options?

---

## 🛡️ Reliability & Safety

- Timeout protection
- Safe fallback responses
- Input validation
- Graceful error handling
- Structured logging

---

## 🌱 Future Improvements

- User authentication
- Decision history
- Multi-agent collaboration
- Personalized memory
- Improved UI animations

---

## 👤 Author

Naviyasri S  
B.Tech Student | AI & Full-Stack Enthusiast

---

## 🏁 Why This Project Stands Out

- Uses agent-based AI, not just a chat wrapper
- Strong backend engineering practices
- Clean UX and product flow
- Real-world practical use case
- Easy to extend and scale


