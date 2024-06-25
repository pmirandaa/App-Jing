from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate,login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from utils import bool_param, is_valid_param
from University.models import University
from Sport.models import Sport
from Team.models import Team, PlayerTeam
from Event.models import Event
import json
from Person.serializers import *
from Person.models import getPersonEventRoles  
import pandas as pd
import xlsxwriter
import os
from backend.settings import BASE_DIR



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = self.queryset
        #event = self.request.query_params.get('event')
        username = self.request.query_params.get('username')
        last_name = self.request.query_params.get('last_name')
        first_name = self.request.query_params.get('first_name')
        university = self.request.query_params.get('university')
        sport = self.request.query_params.get('sport')
        if is_valid_param(username):
            queryset = queryset.filter(username=username)
        if is_valid_param(last_name):
            queryset = queryset.filter(last_name__icontains=last_name)
        if is_valid_param(first_name):
            queryset = queryset.filter(name__icontains=first_name)
        if is_valid_param(university):
            queryset = queryset.filter(university=university)
        if is_valid_param(sport):
            queryset = queryset.filter(playerteam__team__sport=sport)
        queryset = queryset.order_by('last_name')
        return queryset
    

@require_POST
def signin_view(request):
    data=json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    pass
    print("hola")

@require_POST
def login_view(request):
    data= json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse({"detail":"Please provide username and password"})
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"detail":"invalid credentials"}, status=400)
    login(request, user)

    a= PersonSerializer(user.person)
    b= list(PER.objects.filter(person=user.person))
    c= PERSerializer(b, many=True)
    d=Event.objects.filter(current=True)
    print(a)
    print(a.data)
    print(b)
    print(c)
    print(c.data)
    print("current event", d.get().name)
    
    return JsonResponse({"details":"Succesfull log","user": a.data, "PER":c.data})

def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail":"You are not logged"})
    logout(request)
    return JsonResponse({"detail":"Succesfully logged out!"})

@ensure_csrf_cookie    
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})
    a= PersonSerializer(request.user.person)
    b= list(PER.objects.filter(person=request.user.person))
    c= PERSerializer(b, many=True)
    print(a)
    print(a.data)
    print(b)
    print(c)
    print(c.data)
    return JsonResponse({"isAuthenticated": True, "user":a.data, "PER":c.data})

def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})
    
    a= PersonSerializer(request.user.person)
    b= list(PER.objects.filter(person=request.user.person))
    c= PERSerializer(b, many=True)
    d=Event.objects.filter(current=True)
    print(a)
    print(a.data)
    print(b)
    print(c)
    print(c.data)
    #print(a.roles)
    #print(a.name)
    
    #print(a.roles.event)
    return JsonResponse({"username": a.data, "PER":c.data})

@require_POST
def DataLoadView(request):
    eventid= request.POST["event"]
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)

    if (request.user.is_authenticated and request.POST['type']== 'teams' and 'organizador' in roles) or "admin" in roles:
        print("carga de equipos")
        data=request.FILES['file']
        print(data)
        post = request.POST
        print(post)
        print(post["event"])
        universityid= request.POST["university"]
        eventid= request.POST["event"]
        print(universityid)
        print(eventid)
        university= University.objects.get(pk=universityid)
        event=Event.objects.get(pk=eventid)

        df = pd.read_excel(data, sheet_name=None)
        print(df)
        for key in df:
            print(key)
            for index,row in df[key].iterrows():
                sport = Sport.objects.get(name=key) #buscar el deport
                eventSport = 0 #buscar el evento deporte EventSport.get()
                #Notar que en este paso ya tengo el deporte y el evento, solo queda crear o buscar el equipo al que agregar la persona.
                nombre=row["nombre"]
                last_name = row["apellido"]
                email = row["email"]
                rut = row["rut"]
                phone_number = row["phone_number"]
                emergency_phone_number =row["emergency_phone"]
                person = Person.objects.filter(rut=rut).first() 
                print(person)

                try:

                    if person: #con esta condici'on se verifica que existe una persona con ese rut en la base de datos
                        print("Existe una persona con ese rut")
                        #revisar el caso borde en que el rut de la persona ya existe
                        #en este caso hay 2 opciones: El usuario puso el rut incorrecto, el rut es correcto y la persona ya esta agregada
                        #custionar si este if debe estar depues de buscar el usuario.
                        #Nueva limitacion de la carga de datos: los usuarios pueden ser a añadidos a equipos y a la base de datos, pero sus datos no pueden ser editados
                    
                        if person.user:
                            print("existe un usuario para la persona")
                            objT, createdT = Team.objects.update_or_create(event=event, sport=sport, university=university)
                            objTP, createdTP = PlayerTeam.objects.update_or_create(player = person, team=objT)
                            
                        else:
                            print("NO existe un usuario para la persona")
                            print("creando usuario")
                            objU, userCreated = User.objects.get_or_create(username = rut) # arreglar el error de user id
                            create_defaults= {'user':objU}
                            objP, createdP = Person.objects.update_or_create(rut=rut,defaults=create_defaults)
                            print(createdP)
                            objT, createdT = Team.objects.update_or_create(event=event, sport=sport, university=university)
                            objTP, createdTP = PlayerTeam.objects.update_or_create(player = objP, team=objT)
                            
                    else:
                        print("NO existe la persona")
                        print("creando usuario")
                        objU, userCreated = User.objects.get_or_create(username = rut) # arreglar el error de user id
                        print(userCreated)
                        create_defaults= {'name':nombre, 'last_name':last_name, 'email':email, 'rut':rut,'university':university,'phone_number':phone_number, 'emergency_phone_number':emergency_phone_number}
                        objP, createdP = Person.objects.update_or_create(user=objU,defaults=create_defaults)
                        print(objP)
                        objT, createdT = Team.objects.update_or_create(event=event, sport=sport, university=university)
                        print(createdT)
                        objTP, createdTP = PlayerTeam.objects.update_or_create(player = objP, team=objT)
                        print(createdTP)

                except ValueError as e:
                    return JsonResponse({"detail": "Error", "Error":str(e)})

        return JsonResponse({"detail": "Data Loades"})
    
    return JsonResponse({"detail": "Not authenticated"})

@require_POST
def PersonDataLoadView(request):
    eventid= request.POST["event"]
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)

    if request.user.is_authenticated and 'organizador' in roles: #aca debo buscar si los permisos del usuario calzan, notar que la subida de datos para personas y usuarios es universal
        print("carga solo de personas")
        a= PersonSerializer(request.user.person)
        b= list(PER.objects.filter(person=request.user.person))
        c= PERSerializer(b, many=True)
        b=Event.objects.filter(current=True)
        data=request.FILES['file']
        print(data)
        #excel_file=data.get('files')
        df = pd.read_excel(data, sheet_name=0)
        print(request.POST)
        print(request.POST["university"])
        print(request.scheme)
        universityid= request.POST["university"]
        university= University.objects.get(pk=universityid)
        error=[]
        error_row=[]
        content=[]
        for index,row in df.iterrows():
            nombre=row["nombre"]
            last_name = row["apellido"]
            email = row["email"]
            rut = row["rut"]
            phone_number = row["phone_number"]
            emergency_phone_number =row["emergency_phone"]
            if Person.objects.filter(rut=rut):
                error.append("Ya existe una persona con ese rut")
                error_row.append(index+2)
                content.append(rut)
                print(index)
                print(error_row)
                print(type(index))
                print(type(error_row))
                # Si hay algun error en las validaciones, se detiene completamente
                # continue (si se quiere continuar la carga e informar de los errores depues, dejar esta linea y borrar el return)
                return JsonResponse({"detail": "Error", "Error":error, "row":error_row, "content":content })
            objU = User.objects.create_user(username= rut, password=rut)
            objP, created = Person.objects.update_or_create(user=objU,name=nombre, last_name=last_name, email=email, rut=rut,university=university,phone_number=phone_number, emergency_phone_number=emergency_phone_number)
            
            print(nombre)
            print(last_name)
            print(email)
            print(university)
            print(rut)
            print(phone_number)
        print(c)
        return JsonResponse({"detail": "Data Loades", "error": error})

    return JsonResponse({"detail": "Not authenticated"})

@require_POST
def MatchDataLoadView(request):
    eventid= request.POST["event"]
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)

    if request.user.is_authenticated and 'organizador' in roles: #aca debo buscar si los permisos del usuario calzan, notar que la subida de datos para personas y usuarios es universal
        print("carga solo de personas")
        b= list(PER.objects.filter(person=request.user.person))
        c= PERSerializer(b, many=True)
        b=Event.objects.filter(current=True)
        data=request.FILES['file']
        print(data)
        #excel_file=data.get('files')
        df = pd.read_excel(data, sheet_name=0)
        print(request.POST)
        print(request.POST["university"])
        print(request.scheme)
        universityid= request.POST["university"]
        university= University.objects.get(pk=universityid)
        error=[]
        error_row=[]
        content=[]
        for index,row in df.iterrows():
            nombre=row["nombre"]
            last_name = row["apellido"]
            email = row["email"]
            rut = row["rut"]
            phone_number = row["phone_number"]
            emergency_phone_number =row["emergency_phone"]
            if Person.objects.filter(rut=rut):
                error.append(rut)
                error.append(row)
                # Si hay algun error en las validaciones, se detiene completamente
                # continue (si se quiere continuar la carga e informar de los errores depues, dejar esta linea y borrar el return)
                return JsonResponse({"detail": "Error", "Error":error, "row":error_row })
            objU = User.objects.create_user(username= rut, password=rut)
            objP, created = Person.objects.update_or_create(user=objU,name=nombre, last_name=last_name, email=email, rut=rut,university=university,phone_number=phone_number, emergency_phone_number=emergency_phone_number)
            
            print(nombre)
            print(last_name)
            print(email)
            print(university)
            print(rut)
            print(phone_number)
        return JsonResponse({"detail": "Data Loades"})

    return JsonResponse({"detail": "Not authenticated"})

def sendExcel(request):

    if request.user.is_authenticated:
        #a= request.POST['sports'] esta deberia ser una lista de deportes para agregar al excel comohojas
        print(request.POST)
        print(request.scheme)
        a= request.POST
        print(a)
        print(a.keys())
        b= a.keys()

        if not b:
            b=["Personas"]

        
        workbook= xlsxwriter.Workbook("Carga.xlsx",{"in_memory": True})
        #datos para agregar gente a un equipo
        # 1 Datos de la persona nombre, apellido, email, university, rut, telefono
        # 2 tener el deporte y el evento, el deporte no se agrega aqui pues lo incluye la hoja del excel
        for key in b:
            print(key)
            worksheet= workbook.add_worksheet(key)
            worksheet.write(0, 0, "nombre")
            worksheet.write(0, 1, "apellido")
            worksheet.write(0, 2, "email")
            worksheet.write(0, 3, "rut")
            worksheet.write(0, 4, "phone_number")
            worksheet.write(0, 5, "emergency_phone")

        #al tener devuelta el excel, cada deporte estara separado por hojas
        # Close the workbook before streaming the data.
        workbook.close()
        with open(os.path.join(str(BASE_DIR)+"/", "Carga.xlsx"),'rb') as f:
            data= f.read()
        
        response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition']= 'attachment; filename="Carga.xlsx"'
        return response
    
    return JsonResponse({"detail": "Not authenticated"})


@require_POST
def CreateTeam(request):
    eventid= request.POST["event"]
    print(eventid)
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)
    print(request.user.is_authenticated) 
    if (request.user.is_authenticated  and 'organizador' in roles) or "admin" in roles:
        universityid= request.POST["university"]
        university= University.objects.get(pk=universityid)
        sportid = request.POST["sport"]
        sport= Sport.objects.get(pk=sportid)
        personlist= request.POST["persons"]
        jsonloads=json.loads(personlist)
        #Revisar que las personas sean de una misma universidad
        team =Team.objects.filter(event=event, sport=sport, university=university)
        if team:
            for element in jsonloads:
                person= Person.objects.get(pk=element["value"])
                p=PlayerTeam.objects.create(player=person, team=team.get())
                print(p)

        else:     
            created=Team.objects.create(event=event, sport=sport, university=university)
            print('equipo creado')
            for element in jsonloads:
                person= Person.objects.get(pk=element["value"])
                p=PlayerTeam.objects.create(player=person, team=created)
                print(p)

        return JsonResponse({"detail": "Equipo Creado"})

    print("Sin autenticar")
    return JsonResponse({"detail": "Not authenticated"})

@require_POST
def CreatePerson(request):
    eventid= request.POST["event"]
    print(eventid)
    event=Event.objects.get(pk=eventid)
    roles=getPersonEventRoles(request.user.person,event)
    print(request.user.is_authenticated) 
    if (request.user.is_authenticated  and 'organizador' in roles) or "admin" in roles:
        post =request.POST
        print(post)
        nombre = post['name']
        last_name = post['lastName']
        universityid= post["university"]
        email = post['email']
        rut = post['rut']
        phone_number = post['phone']
        emergency_phone_number = post['emergencyPhone']
        university= University.objects.get(pk=universityid)
        error=[]
        if Person.objects.filter(rut=rut):
            error.append("Ya existe una persona con ese rut")
            return JsonResponse({"detail": "Error", "Error":error})
            
        objU = User.objects.create_user(username= rut, password=rut)
        person= Person.objects.create(user=objU,name=nombre, last_name=last_name, email=email, rut=rut,university=university,phone_number=phone_number, emergency_phone_number=emergency_phone_number)
        
        print("universit id", university)

        return JsonResponse({"detail": "Persona Creada"})
    
    return JsonResponse({"detail": "Not authenticated"})



