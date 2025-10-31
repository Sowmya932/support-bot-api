# model_store.py
import os
import joblib
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, '../../..', 'models')

def load_models():
    clf_path = os.path.join(MODEL_DIR, 'intent_clf.joblib')
    embed_path = os.path.join(MODEL_DIR, 'embedder')
    faiss_path = os.path.join(MODEL_DIR, 'faiss_index.idx')
    resp_path = os.path.join(MODEL_DIR, 'responses.json')

    clf = joblib.load(clf_path)
    embedder = SentenceTransformer(embed_path)
    index = faiss.read_index(faiss_path)
    with open(resp_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    return clf, embedder, index, mapping

def nearest_response(embedder, index, mapping, text, k=1):
    emb = embedder.encode([text], convert_to_numpy=True).astype('float32')
    D, I = index.search(emb, k)
    idx = int(I[0][0])
    return mapping['responses'][idx], mapping['texts'][idx], float(D[0][0])
