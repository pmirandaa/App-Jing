from datetime import datetime
import json
from pprint import pprint
import random
from addresses import random_addresses
from sports import sports
from universities import universities
from admins import admin_person, admin_user
from persons import names, surnames

seed = random.randint(0, 1000000)
seed = 543384
random.seed(seed)
print("Seed:", seed)
with open('backend\data_generator\last_seeds', 'a', encoding='utf-8') as f:
    f.write(f"{datetime.now()} - {seed}\n")

data = []

# Main admin
data.append(admin_user)
data.append(admin_person)

# Events
data_events = []
for i in range(10):
    event = {
        "model": "Event.event",
        "pk": i+1,
        "fields": {
            "name": f"JING {2013+i}",
            "year": 2013+i,
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
                "is_host": hosts[(eve["pk"] - 1) % 8] == uni["pk"]
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
used_usernames = set()
used_ruts = set()
for i in range(10000):
    username = None
    while username is None or username in used_usernames:
        fname = random.choice(names)
        lname = random.choice(surnames)
        username = f"{fname.lower()}.{lname.lower()}"
        username = username.translate(normalize)
    used_usernames.add(username)
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

    full_rut = None
    while full_rut is None or full_rut in used_ruts:
        rut = random.randint(10000000, 30000000)
        dv = random.randint(0, 10)
        dv = "k" if dv == 10 else dv
        full_rut = f"{rut}-{dv}"
    used_ruts.add(full_rut)
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
    for _ in range(2000):
        day = random.randint(15, 17)
        hour = random.randint(9, 19)
        minutes = random.choice(["00", "15", "30", "45"])
        date = f"{eve['fields']['year']}-07-{day}T{hour}:{minutes}:00Z"
        sport = random.randint(1, len(data_sports))
        played = random.choice([True, False])
        closed = False if not played else random.choice([True, False])
        match_count += 1
        mt = {
            "model": "Match.match",
            "pk": match_count,
            "fields": {
                "location": random.randint(1, len(data_locations)),
                "event": random.randint(1, len(data_events)),
                "sport": sport,
                "date": date,
                "played": played,
                "closed": closed,
                "time_finished": "2022-07-16T07:09:50.726Z" if closed else None,
                "comment": "",
            }
        }

        n_teams = random.choices([2, 4, 8], weights=[7, 2, 1])[0]
        used_universities = set()
        eligible_teams = [
            tm for tm in data_teams if tm["fields"]["sport"] == sport and tm["fields"]["event"] == eve["pk"]]
        someone_missing = played and random.random() < 0.5
        whos_missing = random.sample(
            list(range(n_teams)), random.randint(1, n_teams)
        ) if someone_missing else []
        scores = [(random.randint(0, 10) if played and i not in whos_missing else 0)
                  for i in range(n_teams)]
        team = None
        for nt in range(n_teams):
            while (team is None) or (team["fields"]["university"] in used_universities):
                team = random.choice(eligible_teams)
            used_universities.add(team["fields"]["university"])
            attended = played and nt not in whos_missing
            mt_count += 1
            match_team = {
                "model": "Match.matchteam",
                "pk": mt_count,
                "fields": {
                    "team": team["pk"],
                    "match": match_count,
                    "score": scores[nt] if n_teams - len(whos_missing) > 1 else 0,
                    "comment": "Lorem ipsum dolor sit amet" if played and random.random() < 0.3 else "",
                    "is_winner": played and attended and scores[nt] == max(scores),
                    "attended": attended,
                }
            }
            data_match_teams.append(match_team)
        data_matches.append(mt)
data.extend(data_matches)
data.extend(data_match_teams)

# FinalSportPoints
data_sport_points = []
points_dict = {
    "A": {"1": 2000, "2": 1200, "3": 720, "4": 360, "5": 180, "6": 90, "7": 50, "8": 20},
    "B": {"1": 1300, "2": 800, "3": 480, "4": 240, "5": 120, "6": 60, "7": 30, "8": 10},
    "C": {"1": 800, "2": 480, "3": 290, "4": 150, "5": 70, "6": 40, "7": 20, "8": 0}
}
spts_count = 0
for sport_type in points_dict:
    for place in points_dict[sport_type]:
        spts_count += 1
        data_sport_points.append({
            "model": "Sport.finalsportpoints",
            "pk": spts_count,
            "fields": {
                "sport_type": sport_type,
                "place": place,
                "points": points_dict[sport_type][place]
            }
        })
data.extend(data_sport_points)
print("Data generated")
print("Attendance check:")

def bin_search_dict(d, key):
    low = 0
    high = len(d) - 1
    while low <= high:
        mid = (low + high) // 2
        if d[mid]["pk"] == key:
            return d[mid]
        elif d[mid]["pk"] < key:
            low = mid + 1
        else:
            high = mid - 1
    return None

attendance_check = {}
for mt in data_match_teams:
    #if int(mt["pk"]) % 3000 == 0:
    #    print(f"{int(mt['pk'])}/{len(data_match_teams)} ({round(int(mt['pk']) / len(data_match_teams) * 100, 2)}%)")
    match_data = bin_search_dict(data_matches, mt["fields"]["match"])
    team_data = bin_search_dict(data_teams, mt["fields"]["team"])
    event = attendance_check.setdefault(match_data["fields"]["event"], {})
    sport = event.setdefault(match_data["fields"]["sport"], {})
    university = sport.setdefault(team_data["fields"]["university"], {"matches": 0, "attended": 0})
    university["matches"] += 1
    university["attended"] += mt["fields"]["attended"]

attendances = []
zero_attendance = []
for event in attendance_check:
    for sport in attendance_check[event]:
        for university in attendance_check[event][sport]:
            u = attendance_check[event][sport][university]
            u["attendance"] = round(u["attended"] / u["matches"] * 100, 2)
            attendances.append(u["attendance"])
            if u["attendance"] == 0:
                zero_attendance.append({"event": event, "sport": sport, "university": university})

print(f"Lowest attendance: {min(attendances)}%")
print(f"Highest attendance: {max(attendances)}%")
print(f"Average attendance: {round(sum(attendances) / len(attendances), 2)}%")
print(f"Zero attendance:")
pprint(zero_attendance)
print(f"Zero attendance 5-1: {len([z for z in zero_attendance if z['event'] == 5 and z['sport'] == 1])}")

with open('backend\data_generator\\attendance.json', 'w', encoding='utf-8') as f:
    json.dump(attendance_check, f, ensure_ascii=False, indent=1)

print("# Entries:", len(data))
with open('backend\data_generator\generated_fixture.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
