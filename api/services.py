# def calculate_ats_score(resume_text, skills):
#     score = 0

#     if len(resume_text) > 500:
#         score += 20

#     if len(skills) > 3:
#         score += 40

#     keywords = ["project", "developed", "built", "managed"]
#     for k in keywords:
#         if k in resume_text.lower():
#             score += 10

#     return min(score, 100)
# import requests

# def extract_skills_from_text(text):
#     prompt = f"""
#     Extract technical skills from this resume text.
#     Return ONLY a Python list.

#     Text:
#     {text}
#     """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     output = response.json()["response"]

#     try:
#         return eval(output)   # or json parse safer way
#     except:
#         return []
# def match_jobs(resume_skills, jobs):
#     results = []

#     resume_skills = set([s.lower() for s in resume_skills])

#     for job in jobs:
#         job_skills = set([s.lower() for s in job.required_skills])

#         if not job_skills:
#             continue

#         # 🎯 MATCH SCORE
#         matched = resume_skills.intersection(job_skills)

#         match_percent = (len(matched) / len(job_skills)) * 100

#         # ❌ missing skills
#         missing_skills = list(job_skills - resume_skills)

#         # 🔥 boost if key skill exists
#         boost = 0
#         if "python" in matched:
#             boost += 5
#         if "sql" in matched:
#             boost += 3

#         final_score = min(match_percent + boost, 100)

#         results.append({
#             "job": job.title,
#             "match_percent": round(final_score, 2),
#             "missing_skills": missing_skills,
#             "matched_skills": list(matched)
#         })

#     return sorted(results, key=lambda x: x["match_percent"], reverse=True)

#     return sorted(results, key=lambda x: x["match_percent"], reverse=True)
# def skill_gap(resume_skills, job_skills):
#     return list(set(job_skills) - set(resume_skills))
# import requests

# def improve_resume(text):
#     prompt = f"""
#     Improve this resume professionally:
#     - make bullet points strong
#     - add action verbs
#     - make ATS friendly

#     Resume:
#     {text}
#     """

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "llama3",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]
# def extract_skills_from_text(text):
#     common_skills = [
#         "python", "java", "django", "flask",
#         "sql", "react", "node", "html", "css"
#     ]

#     found = []

#     for skill in common_skills:
#         if skill in text.lower():
#             found.append(skill)

#     return found






import re
import requests


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


def match_jobs(resume_skills, jobs):
    results = []

    resume_skills = set([s.lower() for s in resume_skills])

    for job in jobs:
        job_skills = set([s.lower() for s in job.required_skills])

        if not job_skills:
            continue

        matched = resume_skills.intersection(job_skills)
        match_percent = (len(matched) / len(job_skills)) * 100
        missing_skills = list(job_skills - resume_skills)

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


def skill_gap(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))


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


# ---------------- CAREER PATH SUGGESTIONS ----------------
CAREER_PATH_MAP = {
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["python", "django", "node", "sql", "flask"],
    "Full Stack Developer": ["react", "node", "django", "sql", "html", "css"],
    "Data Analyst": ["sql", "python"],
    "ML Engineer": ["python", "java"],
}

def suggest_career_paths(skills):
    skills_lower = set(s.lower() for s in skills)
    suggestions = []

    for role, required in CAREER_PATH_MAP.items():
        required_set = set(required)
        match_count = len(skills_lower & required_set)
        if match_count > 0:
            percent = round((match_count / len(required_set)) * 100, 1)
            matched_str = ", ".join(skills_lower & required_set)
            suggestions.append({
                "title": role,
                "percent_match": percent,
                "description": f"{percent}% skill match based on: {matched_str}"
            })

    suggestions.sort(key=lambda x: x["percent_match"], reverse=True)
    return suggestions[:5]


# ---------------- DETAILED FEEDBACK ----------------
def generate_feedback(text, skills):
    strengths = []
    weaknesses = []
    improvements = []
    missing_sections = []

    text_lower = text.lower()

    if len(skills) >= 5:
        strengths.append("Good variety of technical skills listed")
    else:
        weaknesses.append("Very few technical skills detected")
        improvements.append("Add more relevant technical skills to your resume")

    if "project" not in text_lower:
        missing_sections.append("Projects")
        improvements.append("Add a Projects section showcasing your work")
    else:
        strengths.append("Projects section found")

    if "certification" not in text_lower and "certificate" not in text_lower:
        missing_sections.append("Certifications")

    if "achievement" not in text_lower and "award" not in text_lower:
        missing_sections.append("Achievements")

    if len(text.split()) < 150:
        weaknesses.append("Resume content seems too short")
        improvements.append("Expand on your experience and responsibilities")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvements": improvements,
        "missing_sections": missing_sections
    }


# ---------------- EDUCATION & EXPERIENCE CHECK ----------------
def extract_education_experience(text):
    text_lower = text.lower()

    education = None
    edu_patterns = ["b.tech", "btech", "b.e.", "m.tech", "mtech", "mba", "bca", "mca", "bsc", "msc", "phd"]
    for pattern in edu_patterns:
        if pattern in text_lower:
            education = pattern.upper()
            break

    exp_years = 0
    match = re.search(r"(\d+(\.\d+)?)\s*\+?\s*years?", text_lower)
    if match:
        exp_years = float(match.group(1))

    internship_detected = "intern" in text_lower

    project_count = len(re.findall(r"\bproject\b", text_lower))

    return {
        "education": education or "Not found",
        "experience_years": exp_years,
        "internship_detected": internship_detected,
        "project_count": project_count
    }