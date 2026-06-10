import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Field, Category, Job, Question,InterviewFlow

if Field.objects.count() == 0:

    f1 = Field.objects.create(name="Software Engineering")
    f2 = Field.objects.create(name="Data Science")
    f3 = Field.objects.create(name="Management (MBA)")
    f4 = Field.objects.create(name="Cyber Security")
    f5 = Field.objects.create(name="AI / ML")

    Category.objects.create(name="DSA", field=f1)
    Category.objects.create(name="System Design", field=f1)

    Category.objects.create(name="Machine Learning", field=f2)
    Category.objects.create(name="Python", field=f2)

    Category.objects.create(name="Business Analytics", field=f3)
    Category.objects.create(name="Marketing", field=f3)

    Category.objects.create(name="Network Security", field=f4)
    Category.objects.create(name="Ethical Hacking", field=f4)

    Category.objects.create(name="Deep Learning", field=f5)
    Category.objects.create(name="Generative AI", field=f5)

    print("✅ Fields Added")
if Category.objects.count() == 0:
    # Software Engineering
    Category.objects.get_or_create(name="DSA", field=f1)
    Category.objects.get_or_create(name="Operating System", field=f1)
    Category.objects.get_or_create(name="DBMS", field=f1)
    Category.objects.get_or_create(name="Backend", field=f1)
    Category.objects.get_or_create(name="Web Development", field=f1)

    # Data Science
    Category.objects.get_or_create(name="Machine Learning", field=f2)
    Category.objects.get_or_create(name="Statistics", field=f2)
    Category.objects.get_or_create(name="Data Analysis", field=f2)

    # Management (MBA)
    Category.objects.get_or_create(name="HR", field=f3)

    # Cyber Security
    Category.objects.get_or_create(name="Networking", field=f4)
    Category.objects.get_or_create(name="Ethical Hacking", field=f4)
    Category.objects.get_or_create(name="Cryptography", field=f4)
    Category.objects.get_or_create(name="Cyber Laws", field=f4)

    # AI / ML
    Category.objects.get_or_create(name="Deep Learning", field=f5)
    Category.objects.get_or_create(name="Neural Networks", field=f5)
    Category.objects.get_or_create(name="Classification", field=f5)
    Category.objects.get_or_create(name="Regression", field=f5)
from api.models import Field, Category, Job, Question, InterviewFlow

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Field, Category, Job, Question, InterviewFlow

# ✅ INTERVIEW FLOWS
if InterviewFlow.objects.count() == 0:
    
    for field in Field.objects.all():
        for cat in Category.objects.filter(field=field):
            for i in range(5):
                InterviewFlow.objects.create(
                    field=field,
                    category=cat,
                    category_name=cat.name,
                    step_order=i+1
                )

    print(" Interview Flows Added")
else:
    print(" Flows already exist")

    # DATA SCIENCE
    ds_field = Field.objects.get(name="Data Science")
    for cat in Category.objects.filter(field=ds_field):
        for i in range(5):
            InterviewFlow.objects.create(
                field=ds_field,
                category=cat,
                category_name=cat.name,
                step_order=i+1
            )

    # MANAGEMENT (MBA)
    mba_field = Field.objects.get(name="Management (MBA)")
    for cat in Category.objects.filter(field=mba_field):
        for i in range(5):
            InterviewFlow.objects.create(
                field=mba_field,
                category=cat,
                category_name=cat.name,
                step_order=i+1
            )

    # CYBER SECURITY
    cs_field = Field.objects.get(name="Cyber Security")
    for cat in Category.objects.filter(field=cs_field):
        for i in range(5):
            InterviewFlow.objects.create(
                field=cs_field,
                category=cat,
                category_name=cat.name,
                step_order=i+1
            )

    # AI / ML
    ai_field = Field.objects.get(name="AI / ML")
    for cat in Category.objects.filter(field=ai_field):
        for i in range(5):
            InterviewFlow.objects.create(
                field=ai_field,
                category=cat,
                category_name=cat.name,
                step_order=i+1
            )

    print("✅ Interview Flows Added")
if Job.objects.count() == 0:

    Job.objects.create(
        title="Python Developer",
        description="Develop and maintain Django applications.",
        required_skills=["python", "django", "sql"],
        experience_level="Fresher",

        salary_min=400000,
        salary_max=700000,

        location="Remote",
        is_remote=True,

        company="TCS",

        experience_min=0,
        experience_max=1,

        job_type="full_time"
    )

    Job.objects.create(
        title="React Developer",
        description="Build frontend applications using React.",
        required_skills=["react", "javascript", "html", "css"],
        experience_level="1-2 Years",

        salary_min=500000,
        salary_max=900000,

        location="Bangalore",
        is_remote=False,

        company="Infosys",

        experience_min=1,
        experience_max=2,

        job_type="full_time"
    )

    Job.objects.create(
        title="Data Analyst",
        description="Analyze business data and prepare reports.",
        required_skills=["python", "sql", "excel"],
        experience_level="Fresher",

        salary_min=450000,
        salary_max=800000,

        location="Hyderabad",
        is_remote=True,

        company="Wipro",

        experience_min=0,
        experience_max=1,

        job_type="full_time"
    )

    print("✅ Jobs Added")
if Question.objects.count() == 0:

    data = {
        "Management (MBA)": {
            "HR": [
                "What is Organizational Behavior?",
                "What is HR Analytics?",
                "What is Talent Acquisition?",
                "Leadership vs Management.",
                "What is Conflict Resolution?",
                "What is Payroll Management?",
                "What is Performance Appraisal?",
                "What is Employee Engagement?",
                "Recruitment Process.",
                "What is HR Management?",
            ]
        },
        "Cyber Security": {
            "Cyber Laws": [
                "What are Data Protection Regulations?",
                "What is Intellectual Property in Cyber Space?",
                "What is Identity Theft?",
                "What is Cyber Bullying?",
                "What is Digital Evidence?",
                "What is GDPR?",
                "Data Privacy Laws.",
                "What is Cyber Crime?",
                "IT Act 2000.",
                "What is Cyber Law?",
            ],
            "Cryptography": [
                "What is Key Exchange?",
                "What is SSL/TLS?",
                "Public Key Infrastructure.",
                "Digital Signature.",
                "MD5 vs SHA.",
                "What is Hashing?",
                "What is AES?",
                "What is RSA?",
                "Symmetric vs Asymmetric Encryption.",
                "What is Cryptography?",
            ],
            "Ethical Hacking": [
                "What is OWASP?",
                "What is Phishing?",
                "What is Brute Force Attack?",
                "What is Social Engineering?",
                "What is Kali Linux?",
                "What is Vulnerability Assessment?",
                "Cross Site Scripting (XSS).",
                "SQL Injection.",
                "What is Penetration Testing?",
                "What is Ethical Hacking?",
            ],
            "Networking": [
                "What is Port Number?",
                "What is Network Topology?",
                "What is VPN?",
                "What is a Switch?",
                "What is a Router?",
                "What is a Firewall?",
                "What is HTTP and HTTPS?",
                "What is DNS?",
                "TCP vs UDP.",
                "What is IP Address?",
            ],
        },
        "AI / ML": {
            "Deep Learning": [
                "Applications of Deep Learning.",
                "What is Dropout?",
                "What is Batch Normalization?",
                "What is GPU Training?",
                "What is LSTM?",
                "What is Transfer Learning?",
                "What is Pooling?",
                "What is Convolution?",
                "CNN vs RNN.",
                "What is Deep Learning?",
            ],
            "Neural Networks": [
                "Applications of Neural Networks.",
                "Vanishing Gradient Problem.",
                "What are Weights and Biases?",
                "What is Epoch?",
                "Feed Forward Network.",
                "What is Gradient Descent?",
                "What is Backpropagation?",
                "Activation Functions.",
                "What is a Neuron?",
                "What is a Neural Network?",
            ],
            "Regression": [
                "Overfitting in Regression.",
                "Regression Use Cases.",
                "Assumptions of Linear Regression.",
                "What is Polynomial Regression?",
                "Gradient Descent.",
                "R-Squared Value.",
                "Mean Squared Error.",
                "Multiple Linear Regression.",
                "Linear Regression.",
                "What is Regression?",
            ],
            "Classification": [
                "Classification Use Cases.",
                "Naive Bayes Classifier.",
                "K-Nearest Neighbors.",
                "What is F1 Score?",
                "What is ROC Curve?",
                "Accuracy vs Precision.",
                "Confusion Matrix.",
                "Binary vs Multi-Class Classification.",
                "Logistic Regression.",
                "What is Classification?",
            ],
        },
        "Data Science": {
            "Machine Learning": [
                "Precision vs Recall.",
                "What is Model Evaluation?",
                "What is Feature Engineering?",
                "What is Random Forest?",
                "Explain Decision Trees.",
                "What is Cross Validation?",
                "What is Underfitting?",
                "What is Overfitting?",
                "Supervised vs Unsupervised Learning.",
                "What is Machine Learning?",
            ],
            "Statistics": [
                "Correlation vs Causation.",
                "Population vs Sample.",
                "What is Sampling?",
                "What is P-Value?",
                "What is Normal Distribution?",
                "What is Hypothesis Testing?",
                "Variance vs Standard Deviation.",
                "Standard Deviation.",
                "Mean, Median, Mode.",
                "What is Probability?",
            ],
            "Data Analysis": [
                "What is Missing Data Handling?",
                "Difference between Structured and Unstructured Data.",
                "What is EDA (Exploratory Data Analysis)?",
                "Explain Data Visualization.",
                "What is Outlier Detection?",
                "What is Correlation?",
                "Mean vs Median vs Mode.",
                "What is Data Cleaning?",
                "Steps in Data Analysis.",
                "What is Data Analysis?",
            ],
        },
        "Software Engineering": {
            "Operating System": [
                "What is Multithreading?",
                "What is Semaphore?",
                "First Come First Serve (FCFS) Algorithm.",
                "What is Scheduling?",
                "What is Paging?",
                "Explain Virtual Memory.",
                "What is Context Switching?",
                "What is Deadlock?",
                "Process vs Thread.",
                "What is an Operating System?",
            ],
            "DBMS": [
                "Write a query to find duplicate records.",
                "What is a Transaction?",
                "Difference between SQL and NoSQL.",
                "What are ACID Properties?",
                "What is Indexing?",
                "Types of Joins in SQL.",
                "Explain 1NF, 2NF, 3NF.",
                "What is Normalization?",
                "Primary Key vs Foreign Key.",
                "What is DBMS?",
            ],
            "Backend": [
                "What is Caching?",
                "Explain HTTP Status Codes.",
                "What is Microservices Architecture?",
                "What is API Rate Limiting?",
                "What is ORM?",
                "What is Middleware?",
                "Session vs Cookies.",
                "What is JWT Authentication?",
                "Difference between GET and POST.",
                "What is REST API?",
            ],
            "DSA": [
                "Implement merge sort",
                "Reverse linked list",
                "Reverse a string",
                "Check if a string is palindrome",
                "Loop optimization?",
                "For vs while loop?",
                "Pattern printing.",
                "Break vs continue?",
                "Nested loops example.",
                "Reverse number program.",
                "Prime number check.",
                "Factorial program.",
                "Fibonacci series (coding).",
                "What is loop in Python?",
            ],
            "Web Development": [
                "Important HTML tags?",
                "Navigation bar creation.",
                "HTML vs HTML5?",
                "Form tag usage.",
                "Create table in HTML.",
                "What is semantic HTML?",
                "HTML page structure.",
                "Difference between div and span.",
                "Create login form (code).",
                "What is HTML?",
            ],
        },
    }

    added = 0
    for field_name, categories in data.items():
        field = Field.objects.filter(name=field_name).first()
        if not field:
            print(f"⚠️ Field not found: {field_name}")
            continue
        for category_name, questions in categories.items():
            category = Category.objects.filter(
                name__icontains=category_name, field=field
            ).first()
            if not category:
                print(f"⚠️ Category not found: {category_name} in {field_name}")
                continue
            for q_text in questions:
                Question.objects.get_or_create(
                    question=q_text,
                    category=category,
                    field=field,
                    defaults={"type": "theory"}
                )
                added += 1

    print(f"✅ Questions Added: {added}")