from django.urls import path

from .views import APIView, HtmlView, Process

app_name = "mql"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('api/', APIView.as_view(), name="mql"),
    path('html/', HtmlView.as_view()),
    path('process/', Process.as_view()),
    
]