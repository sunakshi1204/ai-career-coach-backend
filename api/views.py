import code
import json
import requests
import random
import re
import os
from groq import Groq
from unicodedata import category

from PyPDF2 import PdfReader
from isort import file
from .models import Job

from .utils.compiler import run_python, run_java, run_cpp, run_c, run_node, run_html, run_css
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import InterviewSession, Topic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import requests
from .models import InterviewSession, Field, Category
from .models import (
    Field, Category, Question,
    InterviewFlow, InterviewSession, Answer
)
from .utils.evaluator import evaluate_answer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pdfplumber
import docx

from .models import Job
from .services import (
    calculate_ats_score,
    match_jobs,
    improve_resume,
    extract_skills_from_text
)

from pdfminer.high_level import extract_text

def home(request):
    return HttpResponse("""
    <html>
    <head>
        <title>Interview Simulator</title>
        <style>
            body {
                font-family: Arial;
                text-align: center;
                background: #f5f5f5;
            }
            h1 {
                color: #333;
            }
            .container {
                margin-top: 50px;
            }
            a {
                display: block;
                margin: 10px auto;
                padding: 12px;
                width: 250px;
                text-decoration: none;
                background: #2f5bd3;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            a:hover {
                background: #1d3fa8;
            }
        </style>
    </head>
    <body>

        <h1>🚀 Interview Simulator</h1>

        <div class="container">
            <a href="/fields/">🎯 View Fields</a>
            <a href="/register/">📝 Register</a>
            <a href="/login/">🔐 Login</a>
            <a href="/start-interview/">▶ Start Interview</a>
            <a href="/get-next-question/">❓ Get Question</a>
            <a href="/submit-answer/">✍ Submit Answer</a>
            <a href="/profile/">👤 Profile</a>
        </div>

    </body>
    </html>
    """)

# ================== TEMP USER STORE ==================
USERS = {}


# ================== REGISTER ==================
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"message": "Email & password required"}, status=400)

        if email in USERS:
            return JsonResponse({"message": "User already exists"}, status=400)

        USERS[email] = password

        return JsonResponse({"message": "Signup successful"})

    return JsonResponse({"message": "Only POST allowed"}, status=405)


# ================== LOGIN ==================
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        email = data.get("email")
        password = data.get("password")

        if email not in USERS:
            return JsonResponse({"message": "User not found"}, status=404)

        if USERS[email] != password:
            return JsonResponse({"message": "Wrong password"}, status=400)

        return JsonResponse({
            "message": "Login successful",
            "user": email
        })

    return JsonResponse({"message": "Only POST allowed"}, status=405)


# ================== GET FIELDS ==================
@api_view(['GET'])
def get_fields(request):
    fields = Field.objects.all().values("id", "name")
    return Response(fields)


@api_view(['GET'])
def get_categories(request):
    field_id = request.GET.get("field_id")

    if field_id:
        categories = Category.objects.filter(field_id=field_id)
    else:
        categories = Category.objects.all()

    return Response(categories.values("id", "name", "field_id"))


@api_view(['GET'])
def get_topics_by_category(request, category_id):
    topics = Topic.objects.filter(category_id=category_id)

    data = [
        {
            "id": t.id,
            "name": t.name
        }
        for t in topics
    ]
    return Response(data)


@api_view(['POST'])
def start_interview_flow(request, field_id, category_id):

    flow = InterviewFlow.objects.filter(
        field_id=field_id,
        category_id=category_id
    ).order_by('step_order')

    topics = request.data.get("topics") or []

    interview_questions = []

    for step in flow:

        # 🟡 FOLLOW-UP STEP
        if step.category_name.upper() == "FOLLOW_UP":
            interview_questions.append({
                "question_id": None,
                "type": "FOLLOW_UP",
                "question": "Can you explain more?",
                "is_coding": False
            })
            continue

        # 🟢 GET CATEGORY
        category = Category.objects.filter(
            field_id=field_id,
            name__iexact=step.category_name
        ).first()

        if not category:
            continue

        # 🟢 BASE QUERY
        questions = Question.objects.filter(category=category)

        # 🟢 FILTER BY TOPICS
        if topics:
            questions = questions.filter(topic__name__in=topics)

        # 🔥 DSA = ONLY CODING QUESTIONS
        if category.name.lower() == "dsa":
            questions = questions.filter(is_coding=True)

        if questions.exists():
            q = random.choice(questions)

        interview_questions.append({
            "question_id": q.id,
            "type": step.category_name.lower(),
            "question": q.text,
            "is_coding": q.is_coding,
            "input": q.input_example,
            "expected_output": q.expected_output,
            "constraints": q.constraints
        })

    return Response({
        "questions": interview_questions
    })


@api_view(["POST"])
def run_code(request):
    code = request.data.get("code")
    language = request.data.get("language")

    if language == "python":
        output = run_python(code)
    elif language == "java":
        output = run_java(code)
    elif language == "cpp":
        output = run_cpp(code)
    elif language == "c":
        output = run_c(code)
    elif language == "node":
        output = run_node(code)
    elif language == "html":
        output = run_html(code)
    elif language == "css":
        output = run_css(code)
    else:
        output = "Language not supported"

    return Response({
        "output": output
    })


@api_view(['POST'])
def start_interview(request):

    try:
        print("REQUEST DATA:", request.data)

        name = request.data.get("name")
        field_id = request.data.get("field_id")
        category_id = request.data.get("category_id")

        topics = request.data.get("topics", [])

        if not name or not field_id or not category_id:
            return Response({
                "error": "name, field_id, category_id required"
            }, status=400)

        field_id = int(field_id)
        category_id = int(category_id)

        field = Field.objects.filter(id=field_id).first()
        if not field:
            return Response({"error": "Field not found"}, status=404)

        category = Category.objects.filter(id=category_id).first()
        if not category:
            return Response({"error": "Category not found"}, status=404)

        session = InterviewSession.objects.create(
            user_name=name,
            field=field,
            topics=topics,
            category=category,
        )

        return Response({
            "session_id": session.id,
            "message": "Interview started successfully"
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return Response({
            "error": str(e)
        }, status=500)


# ================== GET NEXT QUESTION (FLOW BASED) ==================
@api_view(['POST'])
def get_next_question(request):
    session_id = request.data.get("session_id")
    step = request.data.get("step")

    if session_id is None or step is None:
        return Response({"error": "session_id and step required"}, status=400)

    step = int(step)

    from django.shortcuts import get_object_or_404
    session = get_object_or_404(InterviewSession, id=session_id)

    field_id = session.field_id
    category_id = session.category_id

    session.current_step = step
    session.save()

    flow = list(InterviewFlow.objects.filter(
        field_id=field_id,
        category_id=category_id
    ).order_by('step_order'))

    if not flow:
        return Response({"error": "No flow found for this field+category"})

    if step >= len(flow):
        return Response({"done": True, "message": "Interview complete!"})

    current_step = flow[step]

    if current_step.category_name.upper() == "FOLLOW_UP":
        return Response({
            "question_id": None,
            "type": "FOLLOW_UP",
            "question": "Can you explain more about your last answer?",
            "is_coding": False
        })

    category = Category.objects.filter(id=category_id).first()

    if not category:
        return Response({"error": "Category not found"}, status=404)

    same_category_steps = [
        i for i, f in enumerate(flow)
        if f.category_name == current_step.category_name
    ]

    position_in_category = same_category_steps.index(step)

    questions = list(Question.objects.filter(
        category=category
    ).order_by("id"))

    topics = session.topics
    if topics:
        questions = list(Question.objects.filter(
            category=category,
            topic__name__in=topics
        ).order_by("id"))

    if not questions:
        return Response({"error": f"No questions found for category: {category.name}"})

    if position_in_category >= len(questions):
        position_in_category = position_in_category % len(questions)

    q = questions[position_in_category]

    return Response({
        "question_id": q.id,
        "type": category.name,
        "question": q.text,
        "is_coding": q.is_coding,
        "input": q.input_example if q.is_coding else None,
        "expected_output": q.expected_output if q.is_coding else None,
        "constraints": q.constraints if hasattr(q, "constraints") else None
    })


# ================== SUBMIT ANSWER ==================
def call_groq(prompt):
    api_key = os.environ.get("GROQ_API_KEY", "").strip()  
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    return response.json()["choices"][0]["message"]["content"].strip()
@api_view(['POST'])
def submit_answer(request):

    session_id = request.data.get("session_id")
    question_id = request.data.get("question_id")
    user_answer = request.data.get("answer")

    # ✅ FIX 1: Handle null question_id (FOLLOW_UP questions)
    if not question_id:
        return Response({"feedback": "Follow-up answer noted. Moving on."})

    if not session_id or not user_answer:
        return Response({"error": "Missing data"}, status=400)

    try:
        session = InterviewSession.objects.get(id=session_id)
    except InterviewSession.DoesNotExist:
        return Response({"error": "Invalid session_id"}, status=404)

    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Invalid question_id"}, status=404)

    # ✅ FIX 2: Prevent duplicate submissions for same session + question
    already_answered = Answer.objects.filter(
        session=session,
        question=question
    ).exists()

    if already_answered:
        existing = Answer.objects.filter(session=session, question=question).first()
        return Response({"feedback": f"Already submitted. Score was: {existing.score}/10"})

    # 🔴 CODING QUESTION
    if question.is_coding:
        code_lines = len([l for l in user_answer.strip().split('\n') if l.strip()])

        if user_answer.strip() == "No code submitted" or code_lines == 0:
            score = 0
        elif code_lines < 3:
            score = 4
        elif code_lines < 8:
            score = 6
        elif code_lines < 15:
            score = 8
        else:
            score = 9

        Answer.objects.create(
            session=session,
            question=question,
            answer_text=user_answer,
            score=score
        )
        return Response({"feedback": f"Code received ({code_lines} lines). Score: {score}/10"})

    # ✅ THEORY QUESTIONS
    if len(user_answer.strip()) < 15:
        return Response({"feedback": "Answer too short. Please explain properly."})

    prompt = f"""Evaluate this interview answer. Reply ONLY in this exact format, no extra text:

Interview Readiness: PASS or FAIL
Correctness: X/5
Concept Understanding: X/3
Communication: X/2
Weak Topics: topic1, topic2
Final Verdict: one line
Overall Score: X/10

Question: {question.text}
Answer: {user_answer}"""

    try:
        feedback = call_groq(prompt)
        # client = Groq(api_key=os.environ.get(""))

        # completion = client.chat.completions.create(
        #     model="llama3-8b-8192",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # feedback = completion.choices[0].message.content.strip()

        score = 5
        for line in feedback.split("\n"):
            if "Overall Score:" in line:
                try:
                    score = int(line.split(":")[1].strip().split("/")[0].strip())
                    break
                except:
                    score = 5

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        # ✅ FIX 3: Return a proper error response instead of crashing
        # Save with default score so interview can continue
        Answer.objects.create(
            session=session,
            question=question,
            answer_text=user_answer,
            score=5
        )
        return Response({
            "feedback": f"AI evaluation unavailable (check GROQ_API_KEY). Answer saved with default score.\nError: {str(e)}"
        })

    Answer.objects.create(
        session=session,
        question=question,
        answer_text=user_answer,
        score=score
    )

    total_answers = Answer.objects.filter(session=session).count()
    response_data = {"feedback": feedback}

    if total_answers >= 5:
        answers = Answer.objects.filter(session=session)
        total_score = sum([a.score for a in answers])
        avg = round(total_score / answers.count(), 2)

        strengths = [a.question.text for a in answers if a.score >= 7]
        weaknesses = [a.question.text for a in answers if a.score < 7]

        response_data["analysis"] = {
            "total_questions": answers.count(),
            "average_score": avg,
            "strengths": strengths,
            "weaknesses": weaknesses
        }

    return Response(response_data)


# ================== REPORT ==================
@api_view(['GET'])
def report(request, session_id):
    answers = Answer.objects.filter(session_id=session_id)

    total = sum([a.score for a in answers])
    avg = total / len(answers) if answers else 0

    strengths = []
    weaknesses = []

    for a in answers:
        if a.score >= 7:
            strengths.append(a.question.text)
        else:
            weaknesses.append(a.question.text)

    return Response({
        "average_score": round(avg, 2),
        "total_questions": len(answers),
        "strengths": strengths,
        "weaknesses": weaknesses
    })


# ================== PROFILE ==================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    return Response({
        "name": user.username,
        "email": user.email
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    user.username = request.data.get("name")
    user.email = request.data.get("email")
    user.save()
    return Response({"message": "Profile updated"})


@api_view(['POST'])
def analyze_resume(request):
    file = request.FILES.get("resume")

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        text = extract_text(file)
    except Exception as e:
        return Response({
            "error": f"File processing failed: {str(e)}"
        }, status=400)

    if not text.strip():
        return Response({
            "error": "Could not extract text from resume"
        }, status=400)

    skills = extract_skills_from_text(text)
    ats_score = calculate_ats_score(text, skills)

    jobs = Job.objects.all()
    job_matches = match_jobs(skills, jobs)

    return Response({
        "skills": skills,
        "ats_score": ats_score,
        "job_matches": job_matches
    })


@api_view(['POST'])
def improve_resume_api(request):
    resume_text = request.data.get("resume_text")

    improved = improve_resume(resume_text)

    return Response({
        "improved_resume": improved
    })


def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return " ".join(page.extract_text() or "" for page in pdf.pages).lower()

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs]).lower()

    else:
        return file.read().decode(errors="ignore").lower()


@api_view(['POST'])
def extract_skills(request):
    resume = request.FILES.get("resume")

    if not resume:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        text = extract_text(resume)
    except:
        return Response({"error": "Unsupported file format"}, status=400)

    skill_map = {
        "python": ["python"],
        "django": ["django"],
        "javascript": ["javascript", "js"],
        "react": ["react", "reactjs"],
        "node": ["node", "nodejs", "node.js"],
        "sql": ["sql", "mysql", "postgresql"],
        "html": ["html"],
        "css": ["css"],
        "api": ["api", "rest", "restapi"]
    }

    found_skills = set()

    for main_skill, variants in skill_map.items():
        for v in variants:
            if re.search(rf"\b{re.escape(v)}\b", text):
                found_skills.add(main_skill)
                break

    return Response({
        "skills": list(found_skills)
    })


@api_view(['GET'])
def get_jobs(request):
    jobs = Job.objects.all()

    data = []
    for job in jobs:
        data.append({
            "title": job.title,
            "skills": job.required_skills,
            "experience": job.experience_level
        })

    return Response(data)


@api_view(['POST'])
def jobs_match(request):
    user_skills = set(s.lower() for s in request.data.get("skills", []))

    if not user_skills:
        return Response({
            "error": "Please provide at least one skill"
        }, status=400)

    jobs = Job.objects.all()
    results = []

    for job in jobs:
        required_skills = set(s.lower() for s in job.required_skills)

        if not required_skills:
            continue

        matched = user_skills & required_skills
        missing = required_skills - user_skills

        match_score = round((len(matched) / len(required_skills)) * 100, 2)

        if match_score < 30:
            continue

        results.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_type": job.job_type,
            "experience": job.experience_level,
            "match_score": match_score,
            "matched_skills": list(matched),
            "missing_skills": list(missing),
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return Response({
        "total_matches": len(results),
        "job_matches": results
    })


@api_view(['GET'])
def job_detail(request, id):
    try:
        job = Job.objects.get(id=id)

        return Response({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "job_type": job.job_type,
            "experience": job.experience_level,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "description": job.description,
            "skills": job.required_skills,
            "is_remote": job.is_remote
        })

    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)
@api_view(['GET'])
def delete_web_dev(request):
    Field.objects.filter(name="Web Development").delete()
    return Response({"message": "Deleted!"})