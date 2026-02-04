from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import os


app = FastAPI(title="GenAI SQL Chatbot")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- shared in-memory dataset ----
active_dataframe = None
active_filename = None

@app.get("/")
def root():
    return {"status": "backend running"}

# ---- upload endpoint ----
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global active_dataframe, active_filename

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Only CSV or XLSX allowed"}

        active_dataframe = df
        active_filename = file.filename

        return {
            "message": "Upload successful",
            "rows": len(df),
            "columns": list(df.columns),
        }

    except Exception as e:
        return {"error": str(e)}

# ---- chat endpoint (TEMP, no Gemini yet) ----
@app.post("/chat")
async def chat(body: dict = Body(...)):
    user_msg = body.get("message")
    if not user_msg:
        return {"reply": "Please ask something about the dataset."}

    if active_dataframe is None:
        return {"reply": "No dataset uploaded yet."}

    df = active_dataframe
    data_text = df.head(20).to_string(index=False)

    prompt = f"""
You are a friendly data assistant.

Here is a sample of the dataset:
{data_text}

User question:
{user_msg}

Answer clearly and concisely.
Do not make the Answer lenghtier than necessary.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120
        )
        reply=response.json().get("response", "No response from model.")
        return {"reply": reply}

    except Exception:
        return {
            "reply": (
                "⚠️ AI is temporarily unavailable due to rate limits.\n"
                "Your dataset is loaded correctly. Please retry in a minute."
            )
        }
