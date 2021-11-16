import os
import json

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.http import HttpResponse
from rest_framework import views
from rest_framework.response import Response
from .serializers import UserSerializer, CollegeSerializer, ExamSerializer, AssigmentSerializer, QuestionSerializer, UserAnswersSerializer, CourseSerializer
import csv
import codecs
from pyNumikweb.functions import api
from api.functions import getPreguntas, getQuestions, getExams, users, userAnswers, te, Assigment


variable    = "1"
db = api()

class UserAnswersView(views.APIView):
    def get(self, request):
        data     = []

        userId = request.query_params['userId']
        examId = request.query_params['examId']
        
        data.append({'userId':userId})

        doc_ref = db.collection(u'user').document(userId).collection(u'answers').document(examId)
        
        doc = doc_ref.get()

        dict = doc.to_dict()

        ToJson = dict#json.dumps(dict, sort_keys=True)

        results = ToJson #UserAnswerSerializer(data, many=True).data
        
        return Response(results)

    @classmethod
    def get_extra_actions(cls):
        return []    

class CoursesView(views.APIView):
    def get(self, request):
        data        = []
        
        courseId    = request.GET.get('courseId')
        collegeId   = request.GET.get('collegeId')
        
        if courseId is None:
            
            docs = db.collection('courses').where(u'collegeId', u'==', collegeId).stream()
                        
            for doc in docs:
                data.append({
                "id"                : doc.id,
                "collegeId"         : doc.to_dict().get('collegeId'),
                "description"       : doc.to_dict().get('description'),
                "nivel"             : doc.to_dict().get('nivel')
                
                })
        else:
            
            doc_ref =   db.collection('courses').document(courseId)
            doc = doc_ref.get()
            
            data.append({
            "id"                : doc.id,
            "collegeId"         : doc.to_dict().get('collegeId'),
            "description"       : doc.to_dict().get('description'),
            "nivel"             : doc.to_dict().get('nivel')
            
            })

        results = CourseSerializer(data, many=True).data
        
        return Response(results)

    @classmethod
    def get_extra_actions(cls):
        return [] 

class UserView(views.APIView):

    def get(self, request):
        data = []
        
        courseId = request.query_params['courseId']

        data = users(courseId)
        
        results = UserSerializer(data, many=True).data
        
        return Response(results)

    @classmethod
    def get_extra_actions(cls):
        return []

class QuestionView(views.APIView):

    def get(self, request):
                
        examId = request.query_params['examId']

        data = getQuestions(examId)
                
        results = QuestionSerializer(data, many=True).data
        
        return Response(results)

    @classmethod
    def get_extra_actions(cls):
        return []

class AssigmentView(views.APIView):
    def get(self, request):
        
        idAssigment = request.query_params['id']
        print(idAssigment)
        assigment = Assigment(idAssigment)
        data = [{
            "id":idAssigment,
            "courseId":assigment.courseId,
            "examId":assigment.examId,
            "Tipo":'tipo',
            "nombreExam":'nomexam',
            "state":1,
            "userId":1
        }]

        results = AssigmentSerializer(data, many=True).data

        return Response(results)
    
    @classmethod
    def get_extra_actions(cls):
        return []

class CollegeView(views.APIView):
    def get(self, request):
        data = []

        colleges_ref = db.collection(u'college')
        docs = colleges_ref.stream()

        for doc in docs:
            data.append({"id": doc.id, "dominio": doc.to_dict().get('dominio'), "name": doc.to_dict().get('name')}) 
        
        results = CollegeSerializer(data, many=True).data

        return Response(results)
    
    @classmethod
    def get_extra_actions(cls):
        return []

class ProgressView(views.APIView):
    def get(self, request):
        
        idAssigment = request.GET.get('id')
        
        if idAssigment is None:
            progress = 'query failed'
        else:
            cont = 1
            assigment   = getAssigment(idAssigment)
            preguntas = len(getPreguntas(assigment['examId']))
            alumnos     = users(assigment['courseId'])
        
            for alumno in alumnos:
                cont+= userAnswers(alumno['userId'], assigment['examId'])

            progress = (cont*100)/(preguntas*len(alumnos))

        data = {'progress':progress}

        return Response(data)

    @classmethod
    def get_extra_actions(cls):
        return []

class ExamView(views.APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        
        idExam = request.GET.get('id')
        
        data = getExams(idExam)

        results = ExamSerializer(data, many=True).data

        return Response(results)
    
    @classmethod
    def get_extra_actions(cls):
        return []

class Delete(View):
    def get(self, request):
        
        id = request.GET.get('id')
        
        data=[]
        
        db.collection('exam').document(id).delete()

        questions = db.collection('question').where(u"idEvaluacion", u'==', id).stream()

        for question in questions:
            db.collection('question').document(question.id).delete()
            data.append({question.id})

        return HttpResponse(data)

# class Test2(View):
#     def get(self, request):
#         #  1:  "Artes Visuales";	
# 		#  2:  "Ciencias";
# 		#  3:  "Educación Física y Salud";	
# 		#  4:  "Historia";
# 		#  5:  "Inglés";
# 		#  6:  "Lengua Indígena";
# 		#  7:  "Lenguaje";
# 		#  8:  "Matemática";
#         nivel       = 1
#         asignatura  = 7
#         data        = ''
#         conn        = psycopg2.connect(host="localhost",database="aeduc-23082019", user="postgres", password="1010011010")
#         cur         = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         sql         = 'SELECT * FROM curriculum_nacional.objetivo WHERE nivel_id='+str(nivel)+' AND asignatura_id='+str(asignatura)
#         cur.execute( sql ) 
#         rows = cur.fetchall()

#         for row in rows:
#             oa = {
#             u'Oa'           : row['objetivo'],
#             u'Asignatura'   : row['asignatura_id'],
#             u'Nivel'        : row['nivel_id'],
#             u'Descripcion'  : row['descripcion'],
#             u'level'        : row['nivel_id'],
#             u'subject'      : row['asignatura_id'],

#         }
#             #data+= row['descripcion']
        
#         return HttpResponse(data)
# def labelFromDb():
#     return ''



class TeView(views.APIView):
    
    def post(self, request):
        file        = request.data['file']
        examId      = request.data['examId']
        csv_reader  = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=',')
        line        = 0
        
        for row in csv_reader:
            
            if line == 0:
                header = row
            else:
                i = 0
                especificaciones = {}
            
                for col in row:
                    especificaciones.update( {header[i] : col} )
                    i+=1
                    order = especificaciones['order'] 
                
                del especificaciones['order']

                #print(especificaciones)

                te(examId, order, especificaciones)

            line+=1
        
        return HttpResponse( line )



class Test(View):
    def get(self, request):
        cont = 1
        assigment   = getAssigment('rlzrCLcpJEyj4NHcrqBL')
        preguntas = len(getPreguntas(assigment['examId']))
        alumnos     = users(assigment['courseId'])
        
        for alumno in alumnos:
            cont+= userAnswers(alumno['userId'], assigment['examId'])

        total = (cont*100)/(preguntas*len(alumnos))

        return HttpResponse( total )        

  

