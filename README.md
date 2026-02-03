# GenAI Dataset Chatbot

A full-stack web application that allows users to **upload CSV/XLSX datasets** and **interactively ask questions about the data** using a conversational Generative AI chatbot.

Unlike traditional demos with hardcoded data, this application dynamically adapts to **user-uploaded datasets** and performs AI-driven analysis in real time.

---

## 🚀 Key Features

- 📁 Upload CSV or Excel (XLSX) files
- 💬 Ask natural language questions about the uploaded dataset
- 🧠 AI-powered data analysis using Gemini
- 🔄 Dynamic, schema-agnostic dataset handling
- 🖥️ React-based chat interface
- ⚙️ FastAPI backend
- 🛡️ Graceful handling of AI rate limits and errors

---

## 🏗️ Tech Stack

### Frontend
- React (Vite)
- JavaScript
- CSS

### Backend
- FastAPI (Python)
- Pandas
- Gemini Generative AI API

---

## 📂 Project Structure

genai-sql-app/
├── main.py # FastAPI backend
├── frontend/ # React frontend
│ ├── src/
│ |── package.json
| |--
├── requirements.txt
├── .env # API keys (not committed)
└── README.md

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd genai-sql-app
2️⃣ Backend Setup
Install dependencies:

bash
Copy code
pip install fastapi uvicorn pandas openpyxl python-dotenv google-generativeai
Create a .env file:

env
Copy code
GOOGLE_API_KEY=your_gemini_api_key
Run the backend:

bash
Copy code
uvicorn main:app
Backend will be available at:

arduino
Copy code
http://localhost:8000
3️⃣ Frontend Setup
bash
Copy code
cd frontend
npm install
npm run dev
Frontend will be available at:

arduino
Copy code
http://localhost:5173
🧠 How the System Works
User uploads a CSV/XLSX file via the frontend

Backend reads the file into an in-memory Pandas DataFrame

The chat endpoint uses the uploaded dataset as context

Gemini analyzes a sample of the dataset

AI-generated insights are returned conversationally

If no dataset is uploaded, the system can fall back to default data.

⚠️ Notes & Limitations
Uploaded datasets are stored in memory

Restarting the backend clears uploaded data

Gemini free-tier rate limits apply

Designed primarily for demo and single-user usage

Architecture can be extended for persistence and multi-user support

🔮 Future Enhancements
Persistent dataset storage

Data visualizations and charts

Column-level explanations

Conversation memory

Authentication and multi-user support

🎯 Purpose
This project demonstrates how Generative AI can be combined with real-world datasets to create an intuitive, conversational data analysis experience using modern full-stack technologies.