from django.contrib import admin

from Sport.models import Sport, SportStanding, EventSport, SportCoordinator
from simple_history.admin import SimpleHistoryAdmin
#from Sport.models import FinalSportPoints


class SportAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'gender') #'sport_type', 'coordinator')
    search_fields = ('name', 'gender') #'sport_type', 'coordinator__name')


#class FinalSportPointsAdmin(admin.ModelAdmin):
 #   list_display = ('sport_type', 'place', 'points')
  #  search_fields = ('sport_type', 'place', 'points')
    
class EventSportAdmin(admin.ModelAdmin):
    list_display = ('event', 'sport', 'closed', 'sport_type') 
    search_fields = ('event', 'sport') 

class SportStandingAdmin(SimpleHistoryAdmin):
    list_display = ('event_sport', 'university', 'place', 'participated') 
    search_fields = ('event', 'university') 

class SportCoordinatorAdmin(SimpleHistoryAdmin):
    list_display = ('sport', 'coordinator') 
    search_fields = ('sport', 'gensportder')



admin.site.register(Sport, SportAdmin)
admin.site.register(EventSport, EventSportAdmin)
admin.site.register(SportStanding, SportStandingAdmin)
admin.site.register(SportCoordinator, SportCoordinatorAdmin)
#admin.site.register(FinalSportPoints, FinalSportPointsAdmin)