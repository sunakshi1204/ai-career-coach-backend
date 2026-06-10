import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Field, Category, Job

if Field.objects.count() == 0:
    f1 = Field.objects.create(name="Software Engineering")
    f2 = Field.objects.create(name="Data Science")
    f3 = Field.objects.create(name="Web Development")

    Category.objects.create(name="DSA", field=f1)
    Category.objects.create(name="System Design", field=f1)
    Category.objects.create(name="Machine Learning", field=f2)
    Category.objects.create(name="Python", field=f2)
    Category.objects.create(name="React", field=f3)
    Category.objects.create(name="Django", field=f3)

    print("✅ Data added!")
else:
    print("✅ Data already exists!")

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