from django.conf import settings
import app_jing.settings as app_settings
import django

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES)

django.setup()


from Person.models import Person
from Team.models import Team
from Team.models import PlayerTeam
from Sport.models import Sport
from Event.models import Event

import pandas

excel = pandas.ExcelFile('equipos-universidad-deporte.xlsx')

data = pandas.read_excel(excel, None)
university_id = 4
event = Event.objects.all().first()

for datasheet in data:

    gender = None
    sport = None

    if ' ' in datasheet:
        sport, gender = datasheet.split(' ')[:2]
        if gender != "Damas" and gender != "Varones":
            sport = f'{sport} {gender}'
            gender = None
    
    else:
        if datasheet == "TDM":
            sport = "Tenis de Mesa"
        else:
            sport = datasheet
    
    if gender is not None:
        if gender == "Varones":
            sport = Sport.objects.get(name__iexact=sport, gender=Sport.MALES)
        elif gender == "Damas":
            sport = Sport.objects.get(name__iexact=sport, gender=Sport.FEMALE)

    else:
        sport = Sport.objects.get(name__iexact=sport)
    
    row = 0
    coordinator = None
    players = []

    while True:
        try:
            if data[datasheet].loc[[row]]['nombres'].isnull().item():
                break

            person = Person(
                event=event,
                name=data[datasheet].loc[[row]]['nombres'].item(),
                last_name=f'{data[datasheet].loc[[row]]["apellido paterno"].item()} {data[datasheet].loc[[row]]["apellido materno"].item()}',
                email=data[datasheet].loc[[row]]['email'].item(),
                university_id=university_id,
                rut=data[datasheet].loc[[row]]["rut (12345678-9)"].item(),
                phone_number=data[datasheet].loc[[row]]['telefono(+569XXXXXXXX)'].item(),
                emergency_phone_number=data[datasheet].loc[[row]]['emergencia(+569XXXXXXXX)'].item(),
                is_coach=data[datasheet].loc[[row]]["encargado equipo(si/no)"].item() in ['si', 'Si', 'SI', 'sí', 'Sí', 'SÍ'],
                is_player=data[datasheet].loc[[row]]["encargado equipo(si/no)"].item() in ['no', 'NO', 'No'],
            )

            if person.is_coach:
                coordinator = person

            else:
                players.append(person)
        
            row += 1
        
        except:
            break

    if coordinator is not None:
        coordinator.save()

    team = Team(
        coordinator=coordinator,
        university_id=university_id,
        sport=sport,
        event=event,
    )

    team.save()

    for person in players:
        person.save()

        player_team = PlayerTeam(
            player=person,
            team=team
        )

        player_team.save()

    print(f'Done with {sport}')
    
    print('----------------------------------------------')