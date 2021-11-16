from django.shortcuts import render
from django.views.generic import View
from mql.classes import Query
from django.http import HttpResponse
import json


class APIView(View):
    def get(self, request):
        return render(request, 'query.html')

class HtmlView(View):
    def get(self, request):
        return HttpResponse('cont')

class Process(View):
    def post(self, request):
        query  = request.POST['query'].split()
        mql = Query()
        respuesta = mql.process(query)
        return HttpResponse(json.dumps({'response': respuesta}), content_type="application/json")
        


