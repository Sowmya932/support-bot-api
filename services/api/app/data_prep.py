# data_prep.py
import pandas as pd
import re
import os
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOP = set(stopwords.words('english'))

RAW = os.path.join(os.path.dirname(__file__), '../../..', 'data', 'raw', 'chats.csv')
OUT_DIR = os.path.join(os.path.dirname(__file__), '../../..', 'data', 'processed')

os.makedirs(OUT_DIR, exist_ok=True)

def clean(text: str) -> str:
    text = str(text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', ' ', text)
    text = text.lower().strip()
    tokens = [t for t in text.split() if t not in STOP and len(t) > 1]
    return " ".join(tokens)

def prepare():
    df = pd.read_csv(RAW)
    df = df.dropna(subset=['message'])
    df['text'] = df['message'].map(clean)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    train.to_csv(os.path.join(OUT_DIR, 'train.csv'), index=False)
    test.to_csv(os.path.join(OUT_DIR, 'test.csv'), index=False)
    print(f"Saved train/test to {OUT_DIR}")

if __name__ == "__main__":
    prepare()
