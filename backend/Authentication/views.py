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
import json
from Person.serializers import *
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
    print(request)
    print(request.user)
    print(request.user.person)

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

#la carga de datos debe realizarse 
@require_POST
def DataLoadView(request):

    if request.user.is_authenticated and request.POST['tipo']== 'equipos':
        print("carga de equipos")
        a= PersonSerializer(request.user.person)
        b= list(PER.objects.filter(person=request.user.person))
        c= PERSerializer(b, many=True)
        b=Event.objects.filter(current=True)
        data=request.FILES['file']
        print(data)
        universityid= request.POST["university"]
        university= University.objects.get(pk=universityid)

        df = pd.read_excel(data, sheet_name=None)
        print(df)
        for key in df:
            for index,row in df[key].iterrows():
                sport = Sport.objects.get(name=key) #buscar el deport
                eventSport = 0 #buscar el evento deporte EventSport.get()
                #Notar que en este paso ya tengo el deporte y el evento, solo queda crear o buscar el equipo al que agregar la persona.
                #event =b
                # team = Team.object.get(sport=sport, event=event)
                

                nombre=row["nombre"]
                last_name = row["apellido"]
                email = row["email"]
                rut = row["rut"]
                phone_number = row["phone_number"]
                emergency_phone_number =row["emergency_phone"]
                obj1, userCreated = User.objects.get_or_create(username = rut)
                #obj1 = User.objects.create_user(username= rut, password=rut)
                obj, created = Person.objects.update_or_create(user=obj1,name=nombre, last_name=last_name, email=email, rut=rut,university=university,phone_number=phone_number, emergency_phone_number=emergency_phone_number)
            
        return JsonResponse({"username": "Data Loades"})
        


    elif request.user.is_authenticated: #aca debo buscar si los permisos del usuario calzan, notar que la subida de datos para personas y usuarios es universal
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
        for index,row in df.iterrows():
            nombre=row["nombre"]
            last_name = row["apellido"]
            email = row["email"]
            rut = row["rut"]
            phone_number = row["phone_number"]
            emergency_phone_number =row["emergency_phone"]
            obj1 = User.objects.create_user(username= rut, password=rut)
            obj, created = Person.objects.update_or_create(user=obj1,name=nombre, last_name=last_name, email=email, rut=rut,university=university,phone_number=phone_number, emergency_phone_number=emergency_phone_number)
            
            print(nombre)
            print(last_name)
            print(email)
            print(university)
            print(rut)
            print(phone_number)
        print(c)
        return JsonResponse({"username": "Data Loades"})
    print(request.POST)
    print(request.POST["university"])
    print(request.scheme)
    
    return JsonResponse({"username": "Not authenticated"})

@require_POST
def GeneralDataLoadView(request):

    if request.user.is_authenticated: #aca debo buscar si los permisos del usuario calzan, notar que la subida de datos para personas y usuarios es universal
        a= PersonSerializer(request.user.person)
        b= list(PER.objects.filter(person=request.user.person))
        c= PERSerializer(b, many=True)
        b=Event.objects.filter(current=True)
        data=request.FILES['file']
        universityid= request.POST["university"]
        deportesidlist= request.POST["deportes"]
        print(data)

    return JsonResponse({"username": "Not authenticated"})


def sendExcel(request):

    if request.user.is_authenticated:
        #a= request.POST['sports'] esta deberia ser una lista de deportes para agregar al excel comohojas
        workbook= xlsxwriter.Workbook("Carga.xlsx",{"in_memory": True})
        worksheet= workbook.add_worksheet("Dep1")
        worksheet.write(0, 0, "Hello, world!")

        #al tener devuelta el excel, cada deporte estara separado por hojas
        
        # Close the workbook before streaming the data.
        workbook.close()
        with open(os.path.join(str(BASE_DIR)+"/", "Carga.xlsx"),'rb') as f:
            data= f.read()
        
        #data1= os.path.join(str(BASE_DIR) +"/", "Carga.xlsx")
        response = HttpResponse(data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition']= 'attachment; filename="Carga.xlsx"'
        return response
    
    return JsonResponse({"detail": "Not authenticated"})



