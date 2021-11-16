from pyNumikweb.functions import api

class Query:
    def __init__(self):
        self.db = api()
        self.collections    = ['exam', 'user', 'assigments', 'college', 'courses', 'eje', 'oa', 'question', 'video']
        self.crud           = ['muestrame', 'modifica', 'elimina', 'crea']
    
    def process(self, mql):
        print(mql)
        accion = mql[0]
                
        if accion in self.crud:
            return self.muestra(mql)
        else:
            return 'Opción no válida'            
    
    def muestra(self, mql):
        i=0
        if mql[1] == 'colecciones':
            colecciones = [['colecciones'], self.collections]
            return self.table(colecciones)
        else:
            if '[' in mql[1]:
                i=1
            
            if mql[1+i] in self.collections:
                colecciones = Collection()
                 
                if len(mql) > 2+i:
                    if mql[2+i] == 'donde':
                        donde=[mql[3+i],mql[5+i]]
                    
                        return self.table( colecciones.todo(mql[1+i], donde) )    
                    else:
                        return "Opción no válida"
                
                else:
                    return self.table( colecciones.todo(mql[1+i]) )    
            else:
                return "Opción no válida:"+mql[1+i]
    
    def table(self, colecciones, select=None):
        table = '<table class="table"><thead><tr>'
    
        for header in colecciones[0]:
            if select:
                if header in select:
                    table += '<th scope="col">'+header+'</th>'
            else:
                table += '<th scope="col">'+header+'</th>'

        table += '</tr></thead>'
   
        for coleccion in colecciones[1]:
            table +='<tr>'
            
            if type(coleccion) is dict:
                for k,v in coleccion.items():
                    if select:
                        if header in select:
                            table +='<td>'+str(v)+'</td>'
                    else:
                        table +='<td>'+str(v)+'</td>'
            else:
                table +='<td>'+str(coleccion)+'</td>'
        
            table +='</tr>'
        
        table +='</table>'

        return table

class Collection:
    def __init__(self):
        self.db = api()

    def todo(self, collection, where=None):
        if where:
            docs = self.db.collection(collection).where(where[0], u'==', where[1]).stream()
        else:
            doc_ref = self.db.collection(collection)
            docs = doc_ref.stream()
        
        listDocs    = []
        listKeys    = []
        listOrder   = []

        for doc in docs:
            data = {'id':doc.id}
            data.update(doc.to_dict())
                    
            listDocs.append(data)
            keys = data.keys()
            for key in keys:
                if key not in listKeys:
                    listKeys.append(key)

        for listDoc in listDocs:
            dictTemp = {}

            for listKey in listKeys:
                if listKey in listDoc:
                    dictTemp[listKey] = listDoc[listKey] 
                else:
                    dictTemp[listKey] = None
            
            listOrder.append(dictTemp)

        return [listKeys,listOrder]
