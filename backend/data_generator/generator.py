import json
import random
from addresses import random_addresses
from sports import sports
from universities import universities
from admins import admin_person, admin_user
from persons import names, surnames

data = []


# Main admin
data.append(admin_user)
data.append(admin_person)

# Events
data_events = []
for loc in range(5):
    event = {
        "model": "Event.event",
        "pk": loc+1,
        "fields": {
            "name": f"JING {2018+loc}",
            "year": 2018+loc,
            "logo": ""
        }
    }
    data_events.append(event)
data.extend(data_events)


# Universities
data_universities = []
for uni in universities:
    university = {
        "model": "University.university",
        "pk": len(data_universities) + 1,
        "fields": {
            "name": uni["name"],
            "city": uni["city"],
            "overall_score": 0,
            "logo": "",
            "map": "",
            "short_name": uni["short"]
        }
    }

    data_universities.append(university)
data.extend(data_universities)


# University_Event
data_university_event = []
hosts = [*range(1, len(data_universities)+1)]
random.shuffle(hosts)
for eve in data_events:
    for uni in data_universities:
        uni_eve = {
            "model": "University.universityevent",
            "pk": len(data_university_event) + 1,
            "fields": {
                "university": uni["pk"],
                "event": eve["pk"],
                "is_host": hosts[eve["pk"] - 1] == uni["pk"]
            }
        }
        data_university_event.append(uni_eve)
data.extend(data_university_event)


# Locations
locations = [
    "Multicancha Gimnasio",
    "Multicancha Patio Central",
    "Cancha de Tenis",
    "Cancha de Básquetbol",
    "Cancha de Fútbol",
    "Cancha de Vóleibol",
    "Cancha de Atletismo",
    "Piscina A",
    "Piscina B",
    "Sala de Computación A",
    "Sala de Computación B",
    "Online",
    "Sala multiuso",
    "Auditorio A",
    "Auditorio B",
    "Patio Central",
]

data_locations = []
for uni in range(len(universities)):
    for loc in range(len(locations)):
        location = {
            "model": "Location.location",
            "pk": len(data_locations) + 1,
            "fields": {
                "name": locations[loc],
                "address": f"{random.choice(random_addresses)} {str(random.randint(1111,9999))}",
                "university": uni+1
            }
        }
        data_locations.append(location)
data.extend(data_locations)


# Sports
data_sports = []
for spo in sports:
    sport = {
        "model": "Sport.sport",
        "pk": len(data_sports) + 1,
        "fields": {
            "name": spo["name"],
            "gender": spo["gender"],
            "sport_type": spo["type"],
            "coordinator": 1,
            "closed": False
        }
    }
    data_sports.append(sport)
data.extend(data_sports)


# Users
data_users = []
data_persons = []
normalize = str.maketrans("áéíóúñÁÉÍÓÚÑ", "aeiounAEIOUN")
used_usernames = []
for i in range(2000):
    fname = random.choice(names)
    lname = random.choice(surnames)
    username = f"{fname.lower()}.{lname.lower()}"
    username = username.translate(normalize)
    while username in used_usernames:
        fname = random.choice(names)
        lname = random.choice(surnames)
        username = f"{fname.lower()}.{lname.lower()}"
        username = username.translate(normalize)
    used_usernames.append(username)
    user = {
        "model": "auth.user",
        "pk": i+2,  # 1 is admin
        "fields": {
            "password": "pbkdf2_sha256$320000$bPBvLTojrM9FEY3socWDLu$IMWPNCTHlXU08AsdMhA7Ac99jVJGawPc1tH7cJGXHrM=",
            "last_login": "2022-05-25T06:28:27.643Z",
            "is_superuser": False,
            "username": username,
            "first_name": fname,
            "last_name": lname,
            "email": f"{username}@test.test",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2021-09-09T20:55:29.763Z",
            "groups": [],
            "user_permissions": []
        }
    }

    rut = random.randint(10000000, 30000000)
    dv = random.randint(0, 10)
    dv = "k" if dv == 10 else dv
    full_rut = f"{rut}-{dv}"
    person = {
        "model": "Person.person",
        "pk": i+2,
        "fields": {
            "user": i+2,
            "event": random.randint(1, len(data_events)),
            "name": fname,
            "last_name": lname,
            "email": f"{username}@test.test",
            "university": random.randint(1, len(data_universities)),
            "rut": full_rut,
            "phone_number": f"9{random.randint(10000000, 99999999)}",
            "emergency_phone_number": f"9{random.randint(10000000, 99999999)}",
            "is_admin": False,
            "is_organizer": False,
            "is_university_coordinator": False,
            "is_sports_coordinator": False,
            "is_player": False,
            "is_coach": False,
            "has_avatar": False,
            "pending_messages": 0
        }
    }

    data_users.append(user)
    data_persons.append(person)
data.extend(data_users)
data.extend(data_persons)


# Teams
data_teams = []
data_teams_by_event = {}
data_player_teams = []
team_count = 0
pt_count = 0
for eve in data_events:
    teams_by_event = []
    for spo in data_sports:
        for uni in data_universities:
            team_count += 1
            team = {
                "model": "Team.team",
                "pk": team_count,
                "fields": {
                    "coordinator": 1,
                    "university": uni["pk"],
                    "place": 0,
                    "event_score": 0,
                    "sport": spo["pk"],
                    "event": eve["pk"],
                }
            }

            players = random.sample(data_persons, 3)
            for pla in players:
                pt_count += 1
                player_team = {
                    "model": "Team.playerteam",
                    "pk": pt_count,
                    "fields": {
                        "player": pla["pk"],
                        "team": team_count
                    }
                }
                data_player_teams.append(player_team)
            data_teams.append(team)
            teams_by_event.append(team)
    data_teams_by_event[eve["pk"]] = teams_by_event
data.extend(data_teams)
data.extend(data_player_teams)


# Matches
data_matches = []
data_match_teams = []
match_count = 0
mt_count = 0
for eve in data_events:
    data_teams_for_this_event_copy = data_teams_by_event[eve["pk"]].copy()
    for i in range(2000):
        day = random.randint(15, 17)
        hour = random.randint(9, 19)
        minutes = random.choice(["00", "15", "30", "45"])
        date = f"2022-07-{day}T{hour}:{minutes}:00Z"
        state = random.choice(["MTB", "MIF", "MIC"])
        sport = random.randint(1, len(data_sports))
        closed = random.choice([True, False])
        match_count += 1
        match = {
            "model": "Match.match",
            "pk": match_count,
            "fields": {
                "location": random.randint(1, len(data_locations)),
                "event": random.randint(1, len(data_events)),
                "length": random.randint(6, 12)*10,
                "date": date,
                "state": state,
                "sport": sport,
                "closed": closed,
                "time_closed": "2022-07-16T07:09:50.726Z" if closed else None,
                "winner": None
            }
        }

        n_players = random.choices([2, 4, 8], weights=[7, 2, 1])[0]
        used_teams = []
        used_universities = []
        team = random.choice(data_teams)
        for np in range(n_players):
            while (team["pk"] in used_teams) or (team["fields"]["university"] in used_universities):
                team = random.choice(data_teams)
            used_teams.append(team["pk"])
            used_universities.append(team["fields"]["university"])
            mt_count += 1
            match_team = {
                "model": "Match.matchteam",
                "pk": mt_count,
                "fields": {
                    "team": team["pk"],
                    "match": match_count,
                    "score": random.randint(0, 10),
                    "comment": ""
                }
            }
            data_match_teams.append(match_team)
        data_matches.append(match)
data.extend(data_matches)
data.extend(data_match_teams)

print(len(data))
with open('backend\data_generator\generated_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
