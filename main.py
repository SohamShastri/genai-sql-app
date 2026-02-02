from fastapi import FastAPI, Body
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("GEMINI KEY:", os.getenv("AIzaSyBYqgo92PT32WfudCscvSi7AjStqvvo_JU"))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

app = FastAPI(title="GenAI SQL Chatbot (Gemini)")

def get_sales_data():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/chat")
async def chat(body: dict = Body(...)):
    user_msg = body.get("message")
    if not user_msg:
        return {"reply": "Please send a message."}

    data = get_sales_data()
    data_text = "\n".join([f"{d['month']}: {d['revenue']}" for d in data])

    prompt = f"""
Analyze this sales data:
{data_text}

User question:
{user_msg}
"""

    try:
        response = model.generate_content(prompt)
        reply = response.text if hasattr(response, "text") else str(response)

        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Gemini error: {e}"}
