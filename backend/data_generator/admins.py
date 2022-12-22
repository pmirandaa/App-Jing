admin_user = {
    "model": "auth.user",
    "pk": 1,
    "fields": {
        "password": "pbkdf2_sha256$320000$bPBvLTojrM9FEY3socWDLu$IMWPNCTHlXU08AsdMhA7Ac99jVJGawPc1tH7cJGXHrM=",
        "last_login": "2022-05-25T06:28:27.643Z",
        "is_superuser": True,
        "username": "scisneros",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": True,
        "is_active": True,
        "date_joined": "2021-09-09T20:55:29.763Z",
        "groups": [],
        "user_permissions": []
    }
}

admin_person = {
    "model": "Person.person",
    "pk": 1,
    "fields": {
        "user": 1,
        "event": 5,
        "name": "Sebastián",
        "last_name": "Cisneros",
        "email": "asd@asd.asd",
        "university": 1,
        "rut": "18932156-2",
        "phone_number": "912345678",
        "emergency_phone_number": "912345678",
        "pending_messages": 0
    }
}
