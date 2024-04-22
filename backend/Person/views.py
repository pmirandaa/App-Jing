from time import sleep

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from Sport.models import Sport
from University.models import University
from utils import bool_param, is_valid_param
from django.http import JsonResponse

from Person.models import Person, PER
from Person.serializers import PersonSerializer
from Person.serializers import PERSerializer
from Event.models import Event
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,login, logout


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def dispatch(self, request, *args, **kwargs):
        sleep(0.5)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        event = self.request.query_params.get('user')
        last_name = self.request.query_params.get('last_name')
        first_name = self.request.query_params.get('first_name')
        university = self.request.query_params.get('university')
        sport = self.request.query_params.get('sport')
        if is_valid_param(event):
            queryset = queryset.filter(event=event)
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

    @method_decorator(cache_page(60))
    @action(detail=False)
    def filters(self, request):
        data = {}
        event = self.request.query_params.get('event')
        if is_valid_param(event):
            university = University.objects.filter(
                universityevent__event__exact=event).values('pk', 'short_name')
            data["university"] = [
                {"value": x["pk"], "label": x["short_name"]} for x in university]
            sports = Sport.objects.all().values('pk', 'name')
            data["sport"] = [{"value": x["pk"], "label": x["name"]}
                             for x in sports]
        return Response(data)
    
@require_POST
def DataLoadView(request):
    
    
    if request.user.is_authenticated: #aca debo buscar si los permisos del usuario calzan, notar que la subida de datos para personas y usuarios es universal
        a= PersonSerializer(request.user.person)
        b= list(PER.objects.filter(person=request.user.person))
        c= PERSerializer(b, many=True)
        b=Event.objects.filter(current=True)
        print(c)


