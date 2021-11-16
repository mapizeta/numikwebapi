from django.shortcuts import render
from rest_framework import views
from django.views.generic import View
from rest_framework.response import Response
from api.functions import getAnswers, getQuestions, getPreguntas, getExams, users, userAnswers, Assigment, Exam, Pat
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
#import django_tables2 as tables


#Resultado por tipo de especificación
#(tabla especificaciones, respuestas, propiedad)
def graphic0(corrections):
    #print(corrections)
    
    ll = [{'i':0, 'e':0, 'a':0},{'insuficiente':0, 'elemental':0, 'adecuado':0}]
    general = []
    table   = []

    for student in corrections:
        if student['student'] != 'total':
            grade = nota(student['correct'], (student['correct']+student['incorrect']+student['omitted']), 0.6)
            table.append({'student': student['student'], 'correct':student['correct'], 'incorrect':student['incorrect'], 'omitted':student['omitted'], 'achievement':student['achievement'], 'grade':grade})
            ll = learningLevel(student['achievement'], ll)
    
    general.append({'table':table})
    general.append({'percentages':ll[1]})
    
    data = {'general':general}
    
    return data

def learningLevel(achievement, ll):
    if achievement>=70:
        ll[0]['a']+=1
    if achievement>=50 and achievement<70:
        ll[0]['e']+=1
    if achievement<50:
        ll[0]['i']+=1
    
    total = ll[0]['a']+ll[0]['e']+ll[0]['i']
    
    ll[1]['adecuado']       = round( (ll[0]['a']*100)/total, 1)
    ll[1]['elemental']      = round( (ll[0]['e']*100)/total, 1)
    ll[1]['insuficiente']   = round( (ll[0]['i']*100)/total, 1)

    return ll

def graphicStudent(te, corrections, prop):
    
    json        = []
    
    if prop == 'total':
        
        Correct = Incorrect = Omitted = 0
        for correction in corrections[0]['proofreader']:
            if correction == 'O':
                Omitted+=1
            if correction == 'C':
                Correct+=1
            if correction == 'I':
                Incorrect+=1

        total = {'correct':Correct, 'incorrect':Incorrect, 'omitted':Omitted, 'pat':Pat(Correct)}
        json.append(total)

    else:    
        
    
        lenght      = len(te)
        n           = []
        
        for t in te:
            if t[prop] not in n:
                n.append(t[prop])
        
        for a in n:
            i = 0
            correct = 0
            
            for t in te:
                if t[prop] == a:
                    if corrections[0]['proofreader'][i] == 'C':
                        correct+=1
                i+=1
            
            achievement = round( (correct*100)/lenght, 1 )
            json.append({a:achievement})

    return {prop:json}

def graphic1(te, corrections, prop):
    
    html = ''
    cont = 0
    a = {}
    b = {}
    c = []
    props = {}
    ll = [{'i':0, 'e':0, 'a':0},{'insuficiente':0, 'elemental':0, 'adecuado':0}]
    table = []

    for t in te:
        if t[prop] in props:
            props[t[prop]]+= 1
        else:
            props[t[prop]] = 1
        
    for correction in corrections:
        
        if 'proofreader' in correction:
                        
            for result in correction['proofreader']:
                if te[cont][prop] not in a:
                    a[te[cont][prop]] = [0,0,0]
                    
                if te[cont][prop] not in b:
                    b[te[cont][prop]] = [0,0,0]    
                
                if result == 'C':
                    if te[cont][prop] in a:a[te[cont][prop]][0]+=1
                    if te[cont][prop] in b:b[te[cont][prop]][0]+=1
                
                if result == 'I':
                    if te[cont][prop] in a:a[te[cont][prop]][1]+=1
                    if te[cont][prop] in b:b[te[cont][prop]][1]+=1
                
                                       
                cont+=1
            cont = 0

            c.append(b)
            b={}

    data = []
    d = []
    columns = {'student':'Nombre','correct':'Correctas','incorrect':'Incorrectas','achievement':'% Logro'}    
    
    
    for k,v in props.items():
        
        alumno = 0
        
        for n in c:
            if k in n:
                divisor = n[k][0]+n[k][1]
                
                if divisor == 0:
                    achievement = 0
                else:    
                    achievement = round( (n[k][0]*100)/divisor, 2)
                
                data.append({'student':corrections[alumno]['student'], 'correct':n[k][0], 'incorrect':n[k][1],  'achievement':achievement})
                
        #        print(k)
                #print(':')
                #print(achievement)
                #if achievement is not None:
                #    print(k+':'+str(achievement))
                
                ll = learningLevel(achievement, ll)       
        #        print(ll)
            alumno+=1
        print(k)
        print(data)
        print(ll[1])
        d.append({k:[{'table':data},{'percentages':ll[1]}]})
                
        data = []
        ll = [{'i':0, 'e':0, 'a':0},{'insuficiente':0, 'elemental':0, 'adecuado':0}]

    return {prop:d}


def comprobar(te, answers, labelCorrect):
    
    lenght      = len(te)
    cont        = 0
    result      = []
    
    
    tcorrect = tincorrect = tomitted = 0
    for answer in answers:
        correct     = incorrect = omitted = 0
        proofreader = []

        for n in range(lenght):
            num = str(n+1)
            
            if num in answer['answers']:
                
                if answer['answers'][num] == te[n][labelCorrect]:
                    correct+=1
                    proofreader.append('C')
                            
                else:
                    incorrect+=1
                    proofreader.append('I') 
            else:
                omitted+=1
                proofreader.append('O')

        achievement = round( (correct*100)/lenght, 2 ) 
        result.append({
            'student':answer['name'],
            'correct':correct, 
            'incorrect':incorrect, 
            'omitted':omitted,
            'achievement':achievement,
            'proofreader':proofreader,
            })
        cont+=1
    
        tcorrect+=correct
        tincorrect+=incorrect
        tomitted+=omitted
    
    if (lenght*cont) > 0:
        tachievement = round( (tcorrect*100)/(lenght*cont), 2 ) 
    else:
        tachievement = 0

    result.append({'student':'total','correct':tcorrect, 'incorrect':tincorrect, 'omitted':tomitted, 'achievement':tachievement})
    #print(result)
    return result 

def table(columns, students):
    #print(students)
    html = '<table class="responsive-table striped"><thead><tr>'
            
    for k,v in columns.items():
        html+='<th>'+v+'</th>'
    
    html+='</tr></thead>'

    for student in students:
        html+='<tr>'
        
        for k,v in columns.items():
            html+='<td>'+str(student[k])+'</td>'
        
        html+='</tr>'

    html+='</table>'
    
    return html

def graphic2():

    print(result)

def nota(puntaje, puntaje_max, porcentaje_exigencia):
    #puntaje = 29
    #puntaje_max = 30
    #porcentaje_exigencia = 0.6

    minimo_aprobacion = puntaje_max*porcentaje_exigencia

    if puntaje > minimo_aprobacion:
        nota = (puntaje*70)/puntaje_max
    else:
        nota = (puntaje*40)/minimo_aprobacion

    if nota < 20:
        nota = 20.0

    return str(round( (nota/10), 1)).replace(".", ",")

#class NameTable(tables.Table):
    #name = tables.Column()
   
#    class Meta:
#        template_name = "django_tables2/bootstrap4.html"

class APIView(views.APIView):
    def get(self, request):
        assigment   = getAssigment('MXX9DxMGGIlAnSyENpZh')
        students    = users(assigment[0]['courseId'])
        #exam        = getExams(assigment['examId'])
        questions   = getQuestions(assigment[0]['examId'])
        
        te          = buildTe(questions, ['respuestaCorrecta','oa', 'ie'])
        
        answers     = []
        payroll     = []
        for student in students:
                        
            if getAnswers(student['id'],assigment[0]['examId']).to_dict() is not None:
                payroll.append(student['name']+' '+student['surname'])
                arr = getAnswers(student['id'],assigment[0]['examId']).to_dict()
                answers.append(arr) 

        columns = {'student':'Nombre','correct':'Correctas','incorrect':'Incorrectas','achievement':'% Logro'}

        result = comprobar(te,payroll,answers,['respuestaCorrecta','oa', 'ie'])

        #graphic1(te, result)

        print(result)
        #data = {'html':table(columns, result)}
        data = {'html':graphic1(te, result), 'result': [36, 114, 10]}

        return Response(data)
    
    @classmethod
    def get_extra_actions(cls):
        return []

class HtmlView(View):
    def get(self, request):
        data = [
            {"name": "Bradley","surname":"pepito"},
            {"name": "Stevie","surname":"peputo"},
        ]
        
        html = ''
        #graphic2()
        
        return render(request, 'index.html', {'html': html, 'table':NameTable(data,extra_columns=[('name', tables.Column()),('surname', tables.Column())])})

@method_decorator(csrf_exempt, name='dispatch')
class JsonView(views.APIView):
    def get(self, request):
        id  = request.GET.get('id','')
        
        assigment   = Assigment(id)
        data        = Exam(assigment.examId).getTE(['respuestaCorrecta', 'eje', 'oa', 'ie', 'dominio','habilidad'])
        
        result = comprobar(data,assigment.getAnswers(),'respuestaCorrecta')
        res = []
        res.append(graphic0(result))
        res.append(graphic1(data, result, 'eje'))
        res.append(graphic1(data, result, 'oa'))
        res.append(graphic1(data, result, 'ie'))
        res.append(graphic1(data, result, 'dominio'))
        res.append(graphic1(data, result, 'habilidad'))

        response = HttpResponse(json.dumps(res), content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"      
        
        return(response)

@method_decorator(csrf_exempt, name='dispatch')
class StudentView(views.APIView):
    def get(self, request):
        idAssigment  = request.GET.get('idAssigment','')
        idStudent    = request.GET.get('idStudent','')
        
        assigment   = Assigment(idAssigment)
        data        = Exam(assigment.examId).getTE(['respuestaCorrecta', 'eje', 'oa', 'ie', 'dominio','habilidad'])
        
        _answers = assigment.getAnswersStudent(idStudent)
        
        result = comprobar(data,_answers,'respuestaCorrecta')
        res = []
        
        #res.append(graphic0(result))
        #print( graphicStudent(data, result, 'habilidad') )
        res.append(graphicStudent(data, result, 'total'))
        res.append(graphicStudent(data, result, 'eje'))
        #res.append(graphic1(data, result, 'oa'))
        #res.append(graphic1(data, result, 'ie'))
        #res.append(graphic1(data, result, 'dominio'))
        res.append(graphicStudent(data, result, 'habilidad'))

        response = HttpResponse(json.dumps(res), content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"      
        
        return(response)