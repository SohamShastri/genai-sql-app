from fastapi import FastAPI
import sqlite3

app = FastAPI(title="GenAI SQL App")

@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀"}

@app.get("/data")
def get_sales_data():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()

    conn.close()
    return [dict(row) for row in rows]