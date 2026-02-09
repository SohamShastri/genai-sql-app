from asyncio import timeout
from asyncio import timeout
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import pyodbc
import pandas as pd
import ollama 
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
        return {"reply": "Please enter a message."}
        return {"reply": "Please enter a message."}

    if active_dataframe is None:
        return {"reply": "No dataset uploaded yet."}

    df = active_dataframe
    data_text = df.head(20).to_string(index=False)
    prompt = f"""
You are a data assistant.

Rules:
- Answer ONLY using the provided dataset
- Do NOT assume missing information
- Be concise and factual
- If a value is missing, say "Unknown"
- If calculation is needed, compute it from data
- Do NOT add unnecessary explanation

Dataset sample:
{data_text}

User question:
{user_msg}

Answer briefly and clearly.
"""
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response["message"]["content"]

        return {"reply": reply}

    except Exception as e:
        return {
            "reply": f"⚠️ LLaMA Error: {str(e)}"
        }