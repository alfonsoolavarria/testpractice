from models import Profile
import re

class MainTest():
    def __init__(self, request):
        self._request = request
        #self.user = request.user.id
        self._data = None
        self._fields = ['name','phone','company','address','email','gender']
        self.__required = ['name','phone']
        self.response_data = {'error':[], 'data':{}}
        self.code = 200

    def error_confirm(self):
        return True if len(self.response_data['error'])>0 else False

    #para listar un solo usuario
    def get(self,id):
        try:
            one = Profile.objects.get(id=id)
            self.response_data['data'].update({
                'id':one.id,
                'name':one.name,
                'company':one.company if one.company else '',
                'address':one.address if one.address else '',
                'email':one.email if one.email else '',
                'gender':one.gender if one.gender else ''})
        except Exception as e:
             self.response_data['error'] = str(e)
             self.code = 500

    #para lsitar todos los usuarios
    def get_all(self):
        try:
            self.response_data['data'] = []
            users = Profile.objects.all()
            for one in users:
                data={
                    'id':one.id,
                    'name':one.name,
                    'phone':one.phone,
                    'company':one.company if one.company else '',
                    'address':one.address if one.address else '',
                    'email':one.email if one.email else '',
                    'gender':one.gender if one.gender else ''}
                self.response_data['data'].append(data)
        except Exception as e:
             self.response_data['error'] = str(e)
             self.code = 500

    #creacion de un nuevo usuario
    def post(self):
        try:
            self._data = dict((k,self._request.POST[k]) for k in self._fields if k in self._request.POST)
            self.validate()
            if not self.error_confirm():
                self._save()
        except Exception as e:
            print e
            self.code = 500
            self.response_data['error']=str(e)

    def validate(self):
        for k in self.__required:
            if not k in self._request.POST:
                self.response_data['error'].append('Field %s Required' % (k))
                self.code = 409
        if 'name' in self._request.POST and len(self._request.POST['name'])!=0:
            if len(self._request.POST['name'])>100:
                self.response_data['error'] = 'Long Name'
                self.code = 409
                return
            else:self._data['name'] = self.unicode_string(self._data['name'])
        if 'address' in self._request.POST and len(self._request.POST['address'])!=0:
            if len(self._request.POST['address'])>200:
                self.response_data['error'] = 'Long address'
                self.code = 409
                return
            else:self._data['address'] = self.unicode_string(self._data['address'])
        if 'company' in self._request.POST and len(self._request.POST['company'])!=0:
            if len(self._request.POST['company'])>200:
                self.response_data['error'] = 'Long company'
                self.code = 409
                return
            else:self._data['company'] = self.unicode_string(self._data['company'])
        if 'phone' in self._request.POST and len(self._request.POST['phone'])!=0:
            if len(self._request.POST['phone'])>200:
                self.response_data['error'] = 'Long phone'
                self.code = 409
                return
            else:self._data['phone'] = str(self._data['phone'])
        if 'email' in self._request.POST and len(self._request.POST['email'])!=0:
            if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',self._data['email'].lower()):
                self._data['email'] = self.unicode_string(self._data['email'])
            else:
                self.response_data['error'] = 'Long error'
                self.code = 409
                return

    #actualizacion de un usuario
    def put(self,kwargs):
        if 'id' in kwargs:
            self._data = dict((k,self._request.POST[k]) for k in self._fields if k in self._request.POST)
            self.validate()
            if not self.error_confirm():
                self._data.update({'id':int(kwargs['id'])})
                self._save()
        else:
            self.response_data['error']='Id is Required'
            self.code = 500

    #eliminar un registro de usuario
    def delete(self,kwargs):
        if 'id' in kwargs:
            dele=Profile.objects.get(id=kwargs['id'])
            dele.delete()
        else:
            self.response_data['error']='Id is Required'
            self.code = 500

    #-- herramienta la uso para la decodicacion de los caracteres especiales --
    def unicode_string(self,string):
        try:
            st = unicode(string)
            st = st.encode('unicode_escape')
            return st
        except:
            return string

    def decode_string(self,string):
        try:
            return string.decode('unicode_escape')
        except:
            return string

    #metodo para guardar y actualizar
    def _save(self):
        if not 'id' in self._data:
            self.I = Profile(**self._data)
            self.I.save()
        else:
            upda = Profile.objects.filter(id=self._data['id']).update(**self._data)
            self.I = Profile.objects.get(id=self._data['id'])
        self.response_data['data'].update({
            'id':self.I.id,
            'name':self.I.name,
            'phone':self.I.phone,
            'company':self.I.company if self.I.company else None,
            'address':self.I.address if self.I.address else None,
            'email':self.I.email if self.I.email else None,
            'gender':self.I.gender if self.I.gender else None})
        self.code = 201
