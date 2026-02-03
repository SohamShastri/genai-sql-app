from fastapi import FastAPI, Body , UploadFile, File
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd 
active_dataframe = None
active_filename = None

load_dotenv()



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

app = FastAPI(title="GenAI SQL Chatbot (Gemini)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_sales_data():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/upload")
async def upload_file(file: UploadFile = File(...)):
    global active_dataframe, active_filename

    filename = file.filename.lower()
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Unsupported file type. Please upload a CSV or Excel file."}
        active_dataframe=df
        active_filename=file.filename
        return {
                "message": "File uploaded successfully",
                "rows": len(df),
                "columns": list(df.columns)
            }
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}


@app.post("/chat")
async def chat(body: dict = Body(...)):
    user_msg = body.get("message")
    if not user_msg:
        return {"reply": "Please send a message."}

    # Choose dataset
    if active_dataframe is not None:
        df = active_dataframe
        data_text = df.head(20).to_string(index=False)
    else:
        data = get_sales_data()
        data_text = "\n".join([str(row) for row in data])

    prompt = f"""
You are a friendly conversational data assistant.

Dataset sample:
{data_text}

User message:
{user_msg}
Answer conversationally. Be concise unless asked for details.
"""

    response = model.generate_content(prompt)
    return {"reply": response.text}


    prompt = f"""
You are a friendly data assistant.

Here is the dataset (sample rows):
{data_text}

User question:
{user_msg}

Answer conversationally. Be concise unless asked for details.
"""

    try:
        response = model.generate_content(prompt)
        reply = response.text if hasattr(response, "text") else str(response)

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Gemini error: {e}"}
    
   

