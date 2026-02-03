from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

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
    if active_dataframe is None:
        return {"reply": "No dataset uploaded yet."}

    df = active_dataframe
    summary = f"Dataset has {len(df)} rows and {len(df.columns)} columns."

    return {"reply": summary}
