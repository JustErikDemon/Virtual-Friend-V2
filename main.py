from fastapi import FastAPI
import uvicorn
import requests
import urllib.parse
import os

app = FastAPI()

# --- CONFIGURATION ---
API_KEY = "pk_NGG18T1EUVVmvVBz"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 1. HOME
@app.get("/")
def home():
    return {
        "status": "Online",
        "endpoints": {
            "chat": "/ask/{message}",
            "image": "/image/{idea}",
            "face_detector": "/face/{message}"
        }
    }

# 2. CHAT
@app.get("/ask/{message}")
def chat(message: str):
    url = "https://gen.pollinations.ai/v1/chat/completions"
    payload = {
        "model": "gemini-fast",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.5
    }
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        return {"reply": response.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}

# 3. IMAGE LINK
@app.get("/image/{idea}")
def generate_image(idea: str):
    safe_prompt = urllib.parse.quote(idea)
    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?model=flux&width=1024&height=1024&seed=42&nologo=true"
    return {"idea": idea, "link": image_url}

# 4. FACE TEXT DETECTOR
@app.get("/face/{message}")
def detect_face_emotion(message: str):
    url = "https://gen.pollinations.ai/v1/chat/completions"

    instruction = (
        'You are an Emotion AI. You have to pick face for messages. '
        'your faces: "Happy", "curious", "shoked", "sad", "normal", "angry", "annoyed". '
        'Only say the face.'
    )

    payload = {
        "model": "gemini-fast",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": f'message: "{message}"'}
        ],
        "temperature": 0.0
    }

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()

        # Get just the text word (e.g. "annoyed")
        face_name = response.json()["choices"][0]["message"]["content"].strip()

        return {
            "message": message,
            "face": face_name
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
