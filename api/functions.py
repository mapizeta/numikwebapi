from pyNumikweb.functions import api

db = api()

class Assigment:
    
    def __init__(self, assigmentId):
        doc_ref         = db.collection(u'assigments').document(assigmentId)
        doc             = doc_ref.get()
        self.examId     = doc.to_dict().get('examId')
        self.courseId   = doc.to_dict().get('courseId')
    
    
        #self.examId = doc.to_dict().get('examId')

        # data = [{
        #         "id"          : doc.id, 
        #         "Tipo"        : doc.to_dict().get('Tipo'), 
        #         "courseId"    : doc.to_dict().get('courseId'),
        #         "examId"      : doc.to_dict().get('examId'),
        #         "nombreExam"  : doc.to_dict().get('nombreExam'),
        #         "state"       : doc.to_dict().get('state'),
        #         "userId"      : doc.to_dict().get('userId') 
        #     }]

    def getAnswers(self):
        data = []
        students = users(self.courseId)
        for student in students:
            if self._getAnswers(student['id']).to_dict() is not None:
                data.append({'name':student['name']+' '+student['surname'],'answers':self._getAnswers(student['id']).to_dict()})
                
        return data

    def _getAnswers(self, userId):
        doc_ref = db.collection(u'user').document(userId).collection(u'answers').document(self.examId)
        doc = doc_ref.get()
        
        return doc
    
    def getAnswersStudent(self, idUser):
        data = []
        doc_ref         = db.collection(u'user').document(idUser)
        doc             = doc_ref.get()

        if self._getAnswers(idUser).to_dict() is not None:
            data.append({'name':doc.to_dict().get('name')+' '+doc.to_dict().get('surname'),'answers':self._getAnswers(idUser).to_dict()})
        return data

class Exam():
    def __init__(self, examId):
        self.examId = examId
        self.questions = self._questions()

    def _questions(self):
        docs = db.collection(u'question').where(u'idEvaluacion', u'==', self.examId).stream()
        
        data = []                    
        
        for doc in docs:
            
            data.append({
                "id"                :   doc.id,   
                "RespuestaA"        :   doc.to_dict().get('RespuestaA'),
                "RespuestaB"        :   doc.to_dict().get('RespuestaB'),
                "RespuestaC"        :   doc.to_dict().get('RespuestaC'),
                "RespuestaD"        :   doc.to_dict().get('RespuestaD'),
                "code"              :   doc.to_dict().get('code'),
                "dominio"           :   doc.to_dict().get('dominio'),
                "eje"               :   doc.to_dict().get('eje'),
                "habilidad"         :   doc.to_dict().get('habilidad'),
                "idEvaluacion"      :   doc.to_dict().get('idEvaluacion'),
                "ie"                :   doc.to_dict().get('ie'),
                "level"             :   doc.to_dict().get('level'),
                "oa"                :   doc.to_dict().get('oa'),
                "orderInt"          :   int(doc.to_dict().get('order')),
                "order"             :   doc.to_dict().get('order'),
                "owner"             :   doc.to_dict().get('owner'),
                "respuestaCorrecta" :   doc.to_dict().get('respuestaCorrecta'),
                "subject"           :   doc.to_dict().get('subject'),
                "textoPregunta"     :   doc.to_dict().get('textoPregunta'),
                "unidad"            :   doc.to_dict().get('unidad'),
                }) 

        return sorted(data, key = lambda i: i['orderInt'])

    def getTE(self, params):
        te = []
        for question in self.questions:
            aux = {}
            for param in params:
                aux[param] = question[param]
        
            te.append(aux)
        
        return te

def getAnswers(userId, examId):
    doc_ref = db.collection(u'user').document(userId).collection(u'answers').document(examId)
    doc = doc_ref.get()
    return doc


def getExams(idExam = None):
    
    data = []

    if idExam is None:
        docs = db.collection('exam').order_by(u'prueba').stream()
                        
        for doc in docs:
            data.append({
                "id"              : doc.id,
                "Alternativa"     : doc.to_dict().get('Alternativa'),
                "Asignatura"      : doc.to_dict().get('Asignatura'),
                "Nivel"           : doc.to_dict().get('Nivel'),
                "TipoEvaluacion"  : doc.to_dict().get('TipoEvaluacion'),
                "level"           : doc.to_dict().get('level'),
                "owner"           : doc.to_dict().get('owner'),
                "prueba"          : doc.to_dict().get('prueba'),
                "state"           : doc.to_dict().get('state'),
                "subject"         : doc.to_dict().get('subject'),
                "tipo"            : doc.to_dict().get('tipo')
                })
    else:
        doc_ref =   db.collection('exam').document(idExam)
        doc = doc_ref.get()
        
        data.append({
            "id"              : doc.id,
            "Alternativa"     : doc.to_dict().get('Alternativa'),
            "Asignatura"      : doc.to_dict().get('Asignatura'),
            "Nivel"           : doc.to_dict().get('Nivel'),
            "TipoEvaluacion"  : doc.to_dict().get('TipoEvaluacion'),
            "level"           : doc.to_dict().get('level'),
            "owner"           : doc.to_dict().get('owner'),
            "prueba"          : doc.to_dict().get('prueba'),
            "state"           : doc.to_dict().get('state'),
            "subject"         : doc.to_dict().get('subject'),
            "tipo"            : doc.to_dict().get('tipo')
            })
        
    return data

def users(courseId):
    
    docs = db.collection(u'user').where(u'courseId', u'==', courseId).stream()
    data = []    

    for doc in docs:
        data.append({
            "courseId"    : doc.to_dict().get('courseId'),
            "id"          : doc.id, 
            "name": doc.to_dict().get('name'),
            "surname": doc.to_dict().get('surname'), 
            "rut": doc.to_dict().get('rut'),
            "perfil": doc.to_dict().get('perfil'),
            })  
    
    return data

def userAnswers(userId, examId):
    
    doc_ref = db.collection(u'user').document(userId).collection(u'answers').document(examId)
    respuestas = doc_ref.get().to_dict() 
    cont = 0
    if respuestas is None:
        cont = 0
    else:
        for respuesta in respuestas:
            print(respuesta)
            cont+= 1  
    return cont

def getPreguntas(examId):
    
    preguntas = []
    question_ref = db.collection('question').where(u"idEvaluacion", u'==', examId).stream()

    for question in question_ref:
        preguntas.append({
            "correcta"      : question.to_dict().get('respuestaCorrecta'),
            "order"         : question.to_dict().get('order'),
        })

    return preguntas

def getQuestions(examId):
    docs = db.collection(u'question').where(u'idEvaluacion', u'==', examId).stream()
    data = []                    
    
    for doc in docs:
        data.append({
            "id"                :   doc.id,   
            "RespuestaA"        :   doc.to_dict().get('RespuestaA'),
            "RespuestaB"        :   doc.to_dict().get('RespuestaB'),
            "RespuestaC"        :   doc.to_dict().get('RespuestaC'),
            "RespuestaD"        :   doc.to_dict().get('RespuestaD'),
            "code"              :   doc.to_dict().get('code'),
            "dominio"           :   doc.to_dict().get('dominio'),
            "eje"               :   doc.to_dict().get('eje'),
            "habilidad"         :   doc.to_dict().get('habilidad'),
            "idEvaluacion"      :   doc.to_dict().get('idEvaluacion'),
            "ie"                :   doc.to_dict().get('ie'),
            "level"             :   doc.to_dict().get('level'),
            "oa"                :   doc.to_dict().get('oa'),
            "order"             :   doc.to_dict().get('order'),
            "owner"             :   doc.to_dict().get('owner'),
            "respuestaCorrecta" :   doc.to_dict().get('respuestaCorrecta'),
            "subject"           :   doc.to_dict().get('subject'),
            "textoPregunta"     :   doc.to_dict().get('textoPregunta'),
            "unidad"            :   doc.to_dict().get('unidad'),
            }) 
    return data

def getLogro(idAssigment):
    
    doc_ref = db.collection(u'assigments').document(idAssigment)
    doc = doc_ref.get()
    
    examId = doc.to_dict().get('examId')

    #preguntas = getPreguntas(examId)

    return examId
    #return preguntas

def te(examId, order, especificaciones):
        
        question_ref = db.collection('question').where(u"idEvaluacion", u'==', examId).where(u"order", u"==", order).stream()

        for question in question_ref:
            pregunta = db.collection('question').document(question.id)
            pregunta.set(especificaciones, merge=True)
            #pregunta.update(especificaciones)

def Pat(correct):
    pat ={0: 150,1: 159,2: 167,3: 173,4: 189,
5: 200,
6: 213,
7: 219,
8: 226,
9: 232,
10: 240,
11: 254,
12: 271,
13: 280,
14: 297,
15: 321,
16: 346,
17: 367,
18: 390,
19: 410,
20: 419,
21: 435,
22: 453,
23: 470,
24: 486,
25: 499,
26: 512,
27: 523,
28: 532,
29: 535,
30: 542,
31: 549,
32: 557,
33: 564,
34: 570,
35: 576,
36: 582,
37: 587,
38: 593,
39: 595,
40: 600,
41: 604,
42: 608,
43: 612,
44: 617,
45: 621,
46: 625,
47: 629,
48: 633,
49: 637,
50: 641,
51: 645,
52: 648,
53: 651,
54: 655,
55: 658,
56: 662,
57: 666,
58: 669,
59: 673,
60: 677,
61: 681,
62: 686,
63: 690,
64: 694,
65: 698,
66: 703,
67: 707,
68: 712,
69: 717,
70: 723,
71: 728,
72: 736,
73: 742,
74: 750,
75: 762,
76: 775,
77: 789,
78: 808,
79: 832,
80: 850,}
    return pat[correct]
