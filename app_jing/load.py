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

excel = pandas.ExcelFile('excels\PlanillaUC_Vóleibol_Playa_Varones.xlsx')

data = pandas.read_excel(excel, None)
university_id = 2
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
    
    print(f'{sport} - {gender}')

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

            if Person.objects.filter(
                name__icontains=data[datasheet].loc[[row]]['nombres'].item(), 
                last_name__icontains=f'{data[datasheet].loc[[row]]["apellido paterno"].item()} {data[datasheet].loc[[row]]["apellido materno"].item()}'). exists():
                print('esta repetida')

                person = Person.objects.get(
                name__icontains=data[datasheet].loc[[row]]['nombres'].item(), 
                last_name__icontains=f'{data[datasheet].loc[[row]]["apellido paterno"].item()} {data[datasheet].loc[[row]]["apellido materno"].item()}')

            else:
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
                    is_player=data[datasheet].loc[[row]]["encargado equipo(si/no)"].item() in ['no', 'NO', 'No', '', ' '],
                )

            if data[datasheet].loc[[row]]["encargado equipo(si/no)"].item() in ['si', 'Si', 'SI', 'sí', 'Sí', 'SÍ']:
                coordinator = person
                players.append(person)
            else:
                players.append(person)
        
            row += 1
        
        except Exception as e:
            #print(e)
            break

    if coordinator is not None:
        print('COOOORD')
        coordinator.save()

    if Team.objects.filter(
        university_id=university_id,
        sport=sport,
        event=event).exists():

        team = Team.objects.get(
            university_id=university_id,
            sport=sport,
            event=event
        )
    
    else:
        team = Team(
            coordinator=coordinator,
            university_id=university_id,
            sport=sport,
            event=event,
        )

        team.save()

    for person in players:
        person.save()

        if PlayerTeam.objects.filter(player=person, team=team).exists():
            continue

        else:
            player_team = PlayerTeam(
                player=person,
                team=team
            )

            player_team.save()

    print(f'Done with {sport}')
    
    print('----------------------------------------------')