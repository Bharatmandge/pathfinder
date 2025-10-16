from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

# ----- Load environment -----
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
print("Loaded API key:", bool(API_KEY))

# ----- Initialize client -----
client = Groq(api_key=API_KEY)

# ----- FastAPI setup -----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Pydantic model -----
class QuizSubmission(BaseModel):
    answers: dict

# ----- Function to call Groq -----
def analyze_answers(answers):
    prompt = f"""
    Analyze the following quiz answers and suggest the top 5 career paths: {answers}
    
    For each career, provide:
    1. Career title
    2. Brief description
    3. Explanation of why it fits the user based on their answers
    
    Format your response with clear career titles and some detailed explanations.
    Provide exactly 5 career suggestions.
    """
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("Groq API error:", e)
        return "Error fetching career suggestions."

# ----- FastAPI endpoint -----
@app.post("/analyze")
async def analyze(submission: QuizSubmission):
    print("Received submission:", submission.answers)
    career = analyze_answers(submission.answers)
    return {"career": career}
