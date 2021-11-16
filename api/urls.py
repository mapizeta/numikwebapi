from django.urls import path

from .views import UserView, CollegeView, ExamView, AssigmentView, QuestionView, UserAnswersView, CoursesView, TeView, ProgressView


app_name = "api"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('users/', UserView.as_view()),
    path('colleges/', CollegeView.as_view()),
    path('exams/', ExamView.as_view()),
    path('assigments/', AssigmentView.as_view()),
    path('questions/', QuestionView.as_view()),
    path('answers/', UserAnswersView.as_view()),
    path('courses/', CoursesView.as_view()),
    path('te/', TeView.as_view()),
    path('progress', ProgressView.as_view()),
    
]