# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from .model_store import load_models, nearest_response

app = FastAPI(title="Support Bot API")

# load models (on startup)
clf, embedder, index, mapping = load_models()

DB_PATH = os.path.join(os.path.dirname(__file__), '../../..', 'data', 'feedback.db')

class ChatRequest(BaseModel):
    text: str

class Feedback(BaseModel):
    text: str
    intent: str | None = None
    correct: int = 0  # 1 if user says the response was correct, else 0

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    # intent prediction
    emb = embedder.encode([req.text], convert_to_numpy=True)
    intent = clf.predict(emb)[0]
    # nearest response retrieval
    response_text, matched_text, distance = nearest_response(embedder, index, mapping, req.text, k=1)
    return {"intent": intent, "response": response_text, "matched_example": matched_text, "distance": distance}

@app.post("/feedback")
def feedback(payload: Feedback):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS feedback(text TEXT, intent TEXT, correct INTEGER)')
    c.execute('INSERT INTO feedback(text, intent, correct) VALUES (?, ?, ?)', (payload.text, payload.intent or '', int(payload.correct)))
    conn.commit()
    conn.close()
    return {"stored": True}
