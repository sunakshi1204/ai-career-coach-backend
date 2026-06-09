def calculate_ats_score(resume_text, skills):
    score = 0

    if len(resume_text) > 500:
        score += 20

    if len(skills) > 3:
        score += 40

    keywords = ["project", "developed", "built", "managed"]
    for k in keywords:
        if k in resume_text.lower():
            score += 10

    return min(score, 100)
import requests

def extract_skills_from_text(text):
    prompt = f"""
    Extract technical skills from this resume text.
    Return ONLY a Python list.

    Text:
    {text}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    output = response.json()["response"]

    try:
        return eval(output)   # or json parse safer way
    except:
        return []
def match_jobs(resume_skills, jobs):
    results = []

    resume_skills = set([s.lower() for s in resume_skills])

    for job in jobs:
        job_skills = set([s.lower() for s in job.required_skills])

        if not job_skills:
            continue

        # 🎯 MATCH SCORE
        matched = resume_skills.intersection(job_skills)

        match_percent = (len(matched) / len(job_skills)) * 100

        # ❌ missing skills
        missing_skills = list(job_skills - resume_skills)

        # 🔥 boost if key skill exists
        boost = 0
        if "python" in matched:
            boost += 5
        if "sql" in matched:
            boost += 3

        final_score = min(match_percent + boost, 100)

        results.append({
            "job": job.title,
            "match_percent": round(final_score, 2),
            "missing_skills": missing_skills,
            "matched_skills": list(matched)
        })

    return sorted(results, key=lambda x: x["match_percent"], reverse=True)

    return sorted(results, key=lambda x: x["match_percent"], reverse=True)
def skill_gap(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))
import requests

def improve_resume(text):
    prompt = f"""
    Improve this resume professionally:
    - make bullet points strong
    - add action verbs
    - make ATS friendly

    Resume:
    {text}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
def extract_skills_from_text(text):
    common_skills = [
        "python", "java", "django", "flask",
        "sql", "react", "node", "html", "css"
    ]

    found = []

    for skill in common_skills:
        if skill in text.lower():
            found.append(skill)

    return found