from asyncio import timeout
from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import pyodbc
import pandas as pd
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

    if active_dataframe is None:
        return {"reply": "No dataset uploaded yet."}

    df = active_dataframe
    data_text = df.head(20).to_string(index=False)

    prompt = ("""
    "You are a data assistant.\n\n"
    "You are given a dataset sample and a user question.\n\n"
    "Rules:\n"
    "- Answer ONLY using the provided dataset\n"
    "- Do NOT assume missing information\n"
    "- Be concise and factual\n"
    "- If a value is missing, say 'Unknown'\n"
    "- If the question requires counting or calculation, compute it from the dataset\n"
    "- Do NOT add explanations unless asked\n"
    "- Do NOT add examples or stories\n\n"
    "Dataset sample:\n"
    f"{data_text}\n\n"
    "User question:\n"
    f"{user_msg}\n\n"
    "Answer:"
              "Keep the answer brief and to the point."
              "Do not make the answer lengthier than necessary."
    """
)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                 "options": {
                    "num_predict": 120,
                    "temperature": 0.2
                }
            },   
            timeout=120
        )

        reply = response.json().get("response", "No response from model.")
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Local AI error: {e}"}