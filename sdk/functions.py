from firebase_admin import auth, firestore
from firebase_admin.auth import UserRecord
from pyNumikweb.functions import api

class Api:
    def __init__(self):
        self.db = api()

    def createUser(self, data, tipo=None):
        if tipo is not None:
            data['email'] = self.cleanMail(data['name']+data['surname']+data['surname2'])+'@'+str(tipo)
        
        #print(data['email'])
        user = auth.create_user(
             email           =data['email'].strip(),
             email_verified  =False,
             password        =data['rut'].replace('-',''),
             display_name    =data['name'],
             disabled        =False)
        return user.uid
        #return data['email']

    def set_password(self, user_id: str, password: str) -> UserRecord:
        return auth.update_user(user_id, password=password)
    
    def setEmail(self, uid: str, email: str ) -> UserRecord:
        return auth.update_user(uid, email=email)

    def getUsers(self, course):
        doc_ref = self.db.collection('user').where( 'perfil', u'==', 'alumno' ).where( 'courseId', u'==', course )
        docs    = doc_ref.stream()
        return docs
        


    def update(self, collection,document,data):

        doc = self.db.collection(collection).document(document)
        doc.update(data)

    def create(self, collection, document, data):
        self.db.collection(collection).document(document).set(data)
    
    def addFields(self, collection, document, data):
        self.db.collection(collection).document(document).set(data).set(data, merge=True)
    
    def deleteFields(self, collection, data, idEvaluacion):

        doc_ref = self.db.collection(collection).where('idEvaluacion', u'==', idEvaluacion)
        docs    = doc_ref.stream()
        
        for doc in docs:

            update = {}
        
            for d in data:
                update[d] = firestore.DELETE_FIELD
            
            #print(doc.id)
            self.update(collection, doc.id, update)


    def delete(self, collection, document):
        self.db.collection(collection).document(document).delete()

    def documentForm(self, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc = doc_ref.get().to_dict() 
        doc['id'] = document
        return doc

    def user(self):
        cont = 0
        doc_ref = self.db.collection('user')
        docs = doc_ref.stream()
        data='''<thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Id</th>
                    <th scope="col">rut</th>
                    <th scope="col">name</th>
                    <th scope="col">surname</th>
                    <th scope="col">Course</th>
                    <th scope="col">email</th>
                    <th scope="col">Acciones</th>
                </tr>
                </thead>
            '''
        data+= '<tbody>'
        
        for doc in docs:
            cont+=1
            data+='<tr><td scope="row">'+str(cont)+'</th>'    
            data+='<td scope="row"><a href="https://console.firebase.google.com/u/1/project/numik-app/firestore/data~2Fuser~2F'+doc.id+'">'+doc.id+'</a></td>'
            data+='<td>'+str(doc.to_dict().get('rut'))+'</td>'
            data+='<td>'+str(doc.to_dict().get('name'))+'</td>'
            data+='<td>'+str(doc.to_dict().get('surname'))+'</td>'
            data+='<td>'+str(doc.to_dict().get('courseId'))+'</td>'
            data+='<td>'+str(doc.to_dict().get('email'))+'</td>'
            data+='<td scope="row"><a href="/password/?uid='+doc.id+'">Password</a></td>'
        
        data+= '</tbody>'
        
        return data





    def collection(self, collection, attr, where=None, static=None):
        data    = ''
        cont    = 1
        doc_ref = self.db.collection(collection)
        staticDict = ''
        profesor = False

        if where is not None:
            for key in where:
                if key == 'profesor':
                    profesor = True
                else:
                    doc_ref = doc_ref.where( key, u'==', where[key] )
                
        
        docs = doc_ref.stream()
        
        data='''<thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Id</th>
            '''
        for key in attr:
            data+= '<th scope="col">'+key+'</th>'
            if static is not None:
                if key == static:
                    staticDict+=key+"="
        
        if collection == 'user':
            data+= '<th scope="col">Email</th>'

        data+= '<th scope="col">Acciones</th>'
        data+= '</tr></thead>'
        data+= '<tbody>'

        for doc in docs:
            data+='<tr><td scope="row">'+str(cont)+'</th>'    
            data+='<td>'+doc.id+'</td>'                
            
            for key in attr:
                data+='<td>'+str(doc.to_dict().get(key))+'</td>'
            
            if collection == 'user':
                if profesor:
                    data+='<td>'+str(doc.to_dict().get('email'))+'</td>'
                else:
                    data+='<td>'+self.cleanMail( str(doc.to_dict().get('name')).lower()+str(doc.to_dict().get('surname')).lower().replace(" ", "")+str(doc.to_dict().get('surname2')).lower() )+'@'+static.replace('dominio=', '')+'</td>'

            data+='<td><a href="/form/?'+collection+'='+doc.id+'">Editar</a>'
            
            if collection == 'college':
                if static is not None:
                    staticLink = '&static='+staticDict+str(doc.to_dict().get(static))
                    
                data+='&nbsp;&nbsp;&nbsp;<a href="/table/?collection=courses&attributes=description&condition=collegeId='+doc.id+staticLink+'">Cursos</a>'
                data+='&nbsp;&nbsp;&nbsp;<a href="/table/?collection=user&attributes=rut,name,surname&condition=profesor=1,collegeId='+doc.id+staticLink+'">Profesores</a></td>'
            if collection == 'courses':
                if static is not None:
                    staticLink = '&static='+static
                data+='<td><a href="/table/?collection=user&attributes=rut,name,surname&condition=courseId='+doc.id+staticLink+'">Alumnos</a></td>'
            if collection == 'user':
                data+='&nbsp;&nbsp;&nbsp;<a href="/form/?collection=pass&user='+doc.id+'">Reset Pass</a></td>'
            if collection == 'exam':
                data+='<td><a href="/table/?collection=question&attributes=textoPregunta,respuestaCorrecta,order&condition=idEvaluacion='+doc.id+'">Preguntas</a></td>'
                data+='<td><a href="#">Delete</a></td>'

            data+='</tr>'
            cont+= 1

        data+= '</tbody>'

        return data

    def cleanMail(self, email):
        d = {'Á':'a','á':'a','é':'e','í':'i','ó':'o','ú':'u', 'ñ':'n', ' ':''}
        for k,v in d.items():
            email = email.replace(k, v)
        
        return email.lower()