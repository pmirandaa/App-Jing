from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Person.models import Person
from Sport.models import Sport
from University.models import University
from University.serializers import UniversitySerializer

from Administration.models import Log
from Administration.serializers import LogSerializer
from Person.serializers import PersonSerializer
from Placement.permissions import AdminRole, TeamCoordinatorRole, EventCoordinatorRole, UniversityCoordinatorRole, SportCoordinatorRole


class LogViewSet(ModelViewSet):
    serializer_class = LogSerializer
    queryset = Log.objects.all()


class AdminPanelView(APIView):
    permission_classes = [AdminRole | TeamCoordinatorRole | EventCoordinatorRole | UniversityCoordinatorRole | SportCoordinatorRole]

    def get(self, request):

        person = None
        people = PersonSerializer(Person.objects.all(), many=True)
        # events = EventSerializer(Event.objects.all(), many=True)
        universities = UniversitySerializer(
            University.objects.all(), many=True)
        # locations = LocationSerializer(Location.objects.all(), many=True)
        # sports = SportSerializer(Sport.objects.all(), many=True)
        sport_types = Sport.SPORT_TYPE
        genders = Sport.SPORT_GENDER
        # sport_coords = PersonSerializer(Person.objects.filter(is_sports_coordinator=True))
        # unis_coords = PersonSerializer(Person.objects.filter(is_university_coordinator=True))

        if request.user.is_authenticated:
            if Person.objects.filter(user=request.user).exists():
                person = PersonSerializer(Person.objects.get(user=request.user))
                

        data = {
            "name": request.user.username,
            "people": people,
            # "events": events,
            "universities": universities.data,
            # "locations": locations,
            "person": person,
            # "sports": sports,
            "sport_types": sport_types,
            "genders": genders,
            "permissions" : request.user.get_all_permissions(),
            # "sports_coords": sport_coords,
            # "unis_coords": unis_coords,
            # "alert": request.session.pop('alert', None)
        }
        print(data["permissions"])
        print(data)
        return Response(data)
