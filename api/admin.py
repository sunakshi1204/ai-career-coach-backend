from django.contrib import admin
from .models import Field, Category, Job, Question, InterviewFlow, InterviewSession, Answer, Resume, Topic

admin.site.register(Field)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(InterviewFlow)
admin.site.register(InterviewSession)
admin.site.register(Answer)
admin.site.register(Job)
admin.site.register(Resume)