import os
import json
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from pyNumikweb.functions import api
from sdk.functions import Api
import csv
import codecs
from fpdf import FPDF
from pyNumikweb.settings import STATIC_DIR
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import qrcode

sdk = Api()

def password(userId, password):
    sdk.set_password(userId, password)
    return 'password cambiado'

class Update(View):
    def get(self, request):
        return HttpResponse('cont')

class Test(View):
    def where(self, query, collection):
        where = query.index('WHERE')
        docs = collection.where(str(query[where+1]), u'==', str(query[where+3]))
        
        if 'AND' in query:
            And = query.index('AND')
            docs = docs.where(str(query[And+1]), u'==', str(query[And+3]))
        
        return docs


    def get(self, request):
        data ='hola'
        sdk.deleteFields('question', ['dominio', 'habilidad', 'oa', 'ie'], 'NOurPIQ9nNHNWor7xmXm')
        return render(request, 'query.html')

    def post(self, request):
        db = api()
        query  = request.POST['query'].split()
        data = ''

        if query[0] == 'SELECT':
            From = query.index('FROM')

            collection = db.collection(str(query[From+1]))

            if 'WHERE' in query:
                docs = self.where(query, collection)

                docs = docs.stream()
                            
            for doc in docs:
                data+=doc.id+':'+json.dumps(doc.to_dict())+'<br>'
        
        if query[0] == 'UPDATE':
            doc = db.collection(query[1])#.document(document)
            print(query.split('SET')[1].split('WHERE')[0])
            #dict(item.split('=') for item in data.split())

            #doc.update(data)
        
        if query[0] == 'ADD_FIELD':
            collection = db.collection(query[1])
            docs = self.where(query, collection)

            

        return HttpResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class Pdf(View):
    def createQr(self, data):
        qr = qrcode.QRCode(
                version = 1,
                error_correction = qrcode.constants.ERROR_CORRECT_H,
                box_size = 10,
                border = 4,
            )
        stringQr = '{'
        stringQr+= '"surveyApplicationId": "'+data['surveyApplicationId']+'",'
        stringQr+= '"teacher ID": "'+data['teacherID']+'",'
        stringQr+= '"ID": "'+str(data['id'])+'"'
        stringQr+= '}'
        
        qr.add_data(stringQr)
        qr.make(fit=True)
        img = qr.make_image()
        #img.save("image.png")
        image = 'image'+str(data['id'])+'.png'
        
        img.save(os.path.join(STATIC_DIR, image))
        

    def get(self, request):
        output = "Wrong way"
        return HttpResponse(output)

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        #from fpdf import FPDF
        image_path = os.path.join(STATIC_DIR, 'fondoHR.jpg')
        pdf = FPDF(format='letter')
               
        for n in range(data['numberOfPages']):
                        
            if n < 9:
                number = "0"+str(n+1)
            else:
                number = str(n+1)

            dataQr={'surveyApplicationId':data['surveyApplicationId'], 'teacherID':data['teacherID'], 'id':number}
            self.createQr(dataQr)

            imagePathQr = os.path.join(STATIC_DIR, 'image'+str(number)+'.png')
            
            pdf.add_page()
            pdf.set_font("Arial", "B", size=10)
            pdf.image(image_path, x=1, y=1, w=214)
            pdf.image(imagePathQr,x=150, y=41, w=30)
       
            #width, height, txt, border, ln, align
            pdf.set_y(10)
            pdf.cell(5)
            pdf.cell(100, 6, txt="ENCUESTA", ln=2, align="L")
            pdf.set_font("Arial", "B", size=9)
            pdf.cell(100, 8, txt=data['survey'], border=1, ln=2, align="L")
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(100, 6, txt="CURSO", ln=2, align="L")
            pdf.cell(100, 8, txt=data['level'], border=1, ln=2, align="L")
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(100, 6, txt="ASIGNATURA", ln=2, align="L")
            pdf.cell(100, 8, txt=data['subject'], border=1, ln=2, align="L")
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(100, 6, txt="NOMBRE PROFESOR", ln=2, align="L")
            pdf.cell(100, 8, txt=data['teacher'], border=1, ln=2, align="L")
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(100, 6, txt="ESTABLECIMIENTO", ln=2, align="L")
            pdf.cell(100, 8, txt=data['school'], border=1, ln=2, align="L")
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(100, 6, txt="ID", ln=2, align="L")
            pdf.cell(20, 8, txt=number, border=1, ln=2, align="L")

        pdfOut = pdf.output(dest='S').encode('latin-1')
        response = HttpResponse(pdfOut, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        
        return(response)

class Server(View):
    def get(self, request):
        server  = request.GET.get('server','')
        request.session['server'] = server
        return redirect('/')

class Table(View):
    
    def get(self, request):
        if "_auth_user_id" in request.session:
                        
            conditionGet   = request.GET.get('condition',None)
            collectionGet  = request.GET.get('collection','')
            attributesGet  = request.GET.get('attributes','')
            staticGet      = request.GET.get('static','')
            enviroment     = request.GET.get('enviroment','')
            
            attributes  = attributesGet.split(',')
            condition   = {}
            
            if conditionGet is not None:
                key_value = conditionGet.replace('=',':').split(",")
                for v in key_value:
                    aux = v.split(":")
                    condition[aux[0]] = aux[1]
            #print(server)
            sdk = Api()
            html = sdk.collection(collectionGet, attributes, condition, staticGet)
        
            return render(request, 'table.html', {'table': html, 'collection':collectionGet})   
        else:
            return redirect('/')

class User(View):
    def get(self, request):
        if "_auth_user_id" in request.session:
            attributesGet  = request.GET.get('attributes','')
            attributes  = attributesGet.split(',')

            sdk = Api()
            html = sdk.user()

            return render(request, 'users.html', {'table': html})   


class Form(View):
    def get(self, request):
        collection = request.GET.dict().get('collection')
        
        if collection:
            form = {'password': '', 'user':request.GET.dict()['user']}
            k = 'none'
        else:
            document = request.GET.dict()
            [(k, v)] = document.items()
            
            form = sdk.documentForm(k,v) 
            
        return render(request, 'form.html', {'document': form, 'collection': k})

class SendForm(View):
    def get(self, request):
        
        if 'password' in request.GET.dict():
            password(request.GET.dict()['user'], request.GET.dict()['password'])

        else:
            data        = request.GET.dict()
            
            document    = data['id']
            collection  = data['collection']
            referrer    = data['referrer']

            del data['id']
            del data['collection']
            del data['referrer']
            
            sdk.update(collection, document, data)
        
        return redirect(referrer)

class Password(View):
    def get(self, request):
        uid = request.GET.dict().get('uid')
            
        return render(request, 'password.html', {'uid': uid})

class SetPassword(View):
    def get(self, request):
        
        #print(request.GET.dict()['uid']+request.GET.dict()['password'])
        password(request.GET.dict()['uid'],request.GET.dict()['password'])
                
        return redirect('/user')

class SendCsv(View):
    def post(self, request):
        
        collection  = request.POST['collection']
        fields      = request.POST.get('fields','')
        
        file        = request.FILES['file']
        csv_reader  = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=',')
        rowCont     = 0
        output      = ''

        for row in csv_reader:
            rowCont+=1
            data={}
            if rowCont == 1:
                header = row
            else:
                colCont = 0
                for column in header:
                    data[column] = row[colCont]
                    colCont+=1 

                if fields != '':
                    data.update(json.loads(fields))
                
                                
                if not 'email' in header:
                    uid = sdk.createUser(data, 'colegiohermanoscarrera.cl')
                else:
                    uid = sdk.createUser(data)
                #print(data)
                sdk.create(collection, uid, data)
                output+=uid                    
        
        return HttpResponse(output)