from app import db
from app import app
from models import PointTable

with app.app_context():
    db.create_all()

    # Insert dummy data into the PointTable
    dummy_data = [
        {"email": "ali@gmail.com", "name": "Ali", "points": 100},
        {"email": "asghar@gmail.com", "name": "Asghar", "points": 50},
        {"email": "main@gmail.com", "name": "Main", "points": 75},
    ]
    for data in dummy_data:
        point_entry = PointTable(
            email=data["email"], name=data["name"], points=data["points"]
        )
        db.session.add(point_entry)
    print("Tables created successfully")
    db.session.commit()
