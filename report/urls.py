from django.urls import path

from .views import APIView, HtmlView, JsonView, StudentView


app_name = "report"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', APIView.as_view()),
    path('html/', HtmlView.as_view()),
    path('json/', JsonView.as_view()),
    path('studentReport/', StudentView.as_view()),
    
    
]