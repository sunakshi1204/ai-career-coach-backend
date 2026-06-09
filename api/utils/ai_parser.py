import requests
import json

def parse_resume_with_ai(text):
    prompt = f"""
    Extract structured data from resume:
    Return JSON with:
    name, email, phone, skills, experience, education

    Resume:
    {text}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",  # Ollama
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    output = response.json()["response"]

    try:
        return json.loads(output)
    except:
        return {}