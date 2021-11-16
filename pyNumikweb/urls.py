from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from mql.views import APIView, Process
from api.views import Test, Delete
from sdk.views import Table, Form, SendForm, SendCsv, Server, Pdf, Test, Update, User, SetPassword, Password

urlpatterns = [
       
    path('api/', include('api.urls')),
    path('', admin.site.urls, name="admin"),
    path('pdf/', Pdf.as_view(), name="pdf"),
    path('test/', Test.as_view(), name="test"),
    path('update/', Update.as_view(), name="update"),
    path('server/', Server.as_view(), name="server"),
    path('user/', User.as_view(), name="user"),
    path('table/', Table.as_view(), name="table"),
    path('form/', Form.as_view()),
    path('sendForm/', SendForm.as_view()),
    path('password/', Password.as_view()),
    path('setPassword/', SetPassword.as_view()),
    path('sendCsv', SendCsv.as_view()),
    path('delete/', Delete.as_view()),
    path('report/', include('report.urls')),
    path('mql/', APIView.as_view(), name="mql"),
    path('process/', Process.as_view(), name="process"),

    #path('colegios/', ColegioView.as_view()),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

