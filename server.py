from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()


class FoodRequest(BaseModel):
    message: str


@app.get("/check")
def check():
    return {"status": "MCP server running"}


@app.post("/food")
def analyze_food(req: FoodRequest):

    prompt = f"""
Return ONLY valid JSON.

Format:
{{
"calories": number,
"protein": number,
"carbs": number,
"fat": number
}}

Food: {req.message}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        text = response.text.strip()

        data = json.loads(text)
        print(data)

        return data

    except Exception as e:
        return {
            "error": "AI processing failed",
            "details": str(e)
        }