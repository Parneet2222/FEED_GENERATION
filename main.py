from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Load env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ API key not found")

# Initialize LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)

# FastAPI app
app = FastAPI()

# Allow frontend (HTML) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class PostRequest(BaseModel):
    topic: str
    length: str
    language: str


# 🔥 API endpoint
@app.post("/generate")
def generate_post(req: PostRequest):
    try:
        prompt = f"""
        Write a {req.length} LinkedIn post in {req.language} about {req.topic}.

        Make it:
        - Engaging with strong hook
        - Professional
        - Add emojis if suitable
        - Add 3-5 hashtags at end
        """

        response = llm.invoke(prompt)

        return {
            "post": response.content
        }

    except Exception as e:
        return {"error": str(e)}