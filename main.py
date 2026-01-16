from fastapi import FastAPI
import uvicorn
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "instruction": "Add /ask/your-question to the URL"}

@app.get("/ask/{message}")
def chat_with_pollinations(message: str):
    """
    1. Takes the message from the URL.
    2. Sends it to Pollinations AI (Gemini Fast).
    3. Returns the clean AI response.
    """
    
    # The API Endpoint you requested
    url = "https://gen.pollinations.ai/v1/chat/completions"
    
    # The Payload structure
    payload = {
        "model": "gemini-fast",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send POST request to Pollinations
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() # Check for errors
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the specific content based on your example structure
        # choices -> [0] -> message -> content
        ai_reply = data["choices"][0]["message"]["content"]
        
        return {
            "user_message": message,
            "ai_reply": ai_reply,
            # "full_raw_response": data  # Uncomment if you want to see the full JSON
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Run on Replit's open port
    uvicorn.run(app, host="0.0.0.0", port=8080)
