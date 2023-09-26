import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(cred, {
        'databaseURL':"https://facerecognition-58f18-default-rtdb.firebaseio.com/"

})

ref=db.reference('Students')
data={
    "321654":
        {
            "name": "Ashish sharma",
            "Doctor_specialisation": "cardiologist",
            "starting_year": 2021,
            "total_attendance": 7,
            "Availability": "NO",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "Doctor_specialisation": "cardiologist",

            "starting_year": 2021,
            "total_attendance": 12,
            "Availability": "NO",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Dr muskkkk",
            "Doctor_specialisation": "cardiologist",

            "starting_year": 2023,
            "total_attendance": 0,
            "Availability": "YES",
            "year": 2,
            "last_attendance_time": "2023-09-23 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)