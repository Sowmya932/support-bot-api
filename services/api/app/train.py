# train.py
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np
import faiss
import json

BASE_DIR = os.path.dirname(__file__)
PROCESSED = os.path.join(BASE_DIR, '../../..', 'data', 'processed')
MODEL_DIR = os.path.join(BASE_DIR, '../../..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def train():
    train_path = os.path.join(PROCESSED, 'train.csv')
    df = pd.read_csv(train_path)
    texts = df['text'].astype(str).tolist()
    intents = df['intent'].astype(str).tolist()
    responses = df['response'].astype(str).tolist()

    print("Loading embedder...")
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    print("Training classifier...")
    clf = LogisticRegression(max_iter=1000)
    clf.fit(embeddings, intents)

    print("Saving classifier and embedder...")
    joblib.dump(clf, os.path.join(MODEL_DIR, 'intent_clf.joblib'))
    embedder.save(os.path.join(MODEL_DIR, 'embedder'))

    # Build FAISS index for response retrieval
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype('float32'))

    faiss.write_index(index, os.path.join(MODEL_DIR, 'faiss_index.idx'))

    # store response mapping (we will return the nearest training response)
    mapping = {'texts': texts, 'responses': responses}
    with open(os.path.join(MODEL_DIR, 'responses.json'), 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print("Training complete. Models saved to:", MODEL_DIR)

if __name__ == "__main__":
    train()
