# test_api.py
import requests

BASE = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(BASE + "/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_chat():
    r = requests.post(BASE + "/chat", json={"text":"Where is my order?"})
    assert r.status_code == 200
    j = r.json()
    assert "intent" in j and "response" in j
