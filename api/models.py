from unicodedata import name

from django.db import models
from django.utils import timezone
default=timezone.now


#  FIELD (Engineering, MBA, SSB...)
class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


#  CATEGORY (HR, DSA, DBMS...)

class Category(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.field.name} - {self.name}"

class Topic(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
#  QUESTION (MERGED)
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField() 
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) 
    difficulty = models.CharField(max_length=10, default="Easy")

    is_coding = models.BooleanField(default=False)

    input_example = models.TextField(blank=True, null=True)
    expected_output = models.TextField(blank=True, null=True)
    constraints = models.TextField(blank=True, null=True)   # 🔥 yahan

    def __str__(self):
        return self.text


#  INTERVIEW FLOW
# class InterviewFlow(models.Model):
#     field = models.ForeignKey(Field, on_delete=models.CASCADE)
    
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     step_order = models.IntegerField()
#     category_name = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.field.name} - Step {self.step_order}"
class InterviewFlow(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)  # 🔥 ye hona chahiye
    category_name = models.CharField(max_length=100)
    step_order = models.IntegerField()


#  INTERVIEW SESSION (UPDATED)
from django.db import models

class InterviewSession(models.Model):
    user_name = models.CharField(max_length=100)

    field = models.ForeignKey(
        "Field",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    topics = models.JSONField(default=list, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user_name} - {self.field.name}"

#  ANSWERS (UPDATED)
class Answer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer_text = models.TextField(blank=True)   # theory answer
    code = models.TextField(blank=True, null=True)  # coding answer
    output = models.TextField(blank=True, null=True)  # run result

    feedback = models.TextField(blank=True)
    score = models.FloatField(default=0)
class Resume(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    raw_text = models.TextField()
    skills = models.JSONField(default=list)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    ats_score = models.IntegerField(default=0)


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    required_skills = models.JSONField(default=list)

    experience_level = models.CharField(max_length=50)

    # NEW FIELDS
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)

    location = models.CharField(max_length=100, null=True, blank=True)
    is_remote = models.BooleanField(default=False)

    company = models.CharField(max_length=100, null=True, blank=True)

    experience_min = models.IntegerField(default=0)
    experience_max = models.IntegerField(default=2)

    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("internship", "Internship"),
            ("contract", "Contract"),
        ],
        default="full_time"
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0)