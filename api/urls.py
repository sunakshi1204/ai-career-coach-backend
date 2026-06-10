from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register),
    path('login/', views.login),

    path('fields/', views.get_fields),
    path('get-topics/<int:category_id>/', views.get_topics_by_category),
    path('run-code/', views.run_code),
    path('start-interview/', views.start_interview),
    path('start-interview-flow/<int:field_id>/<int:category_id>/', views.start_interview_flow),
    path('get-next-question/', views.get_next_question),
    path('submit-answer/', views.submit_answer),
    path('report/<int:session_id>/', views.report),
    path("analyze-resume/", views.analyze_resume),
    path("improve-resume/", views.improve_resume_api),
    path("extract-skills/", views.extract_skills),
    path("jobs/", views.get_jobs),
    path("jobs-match/", views.jobs_match),
    path('job/<int:id>/', views.job_detail),
    path('delete-web-dev/', views.delete_web_dev),

    path('profile/', views.get_profile),
    path('update-profile/', views.update_profile),
    path('categories/', views.get_categories),
]