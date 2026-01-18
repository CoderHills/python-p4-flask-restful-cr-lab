# server/seed.py

from app import app
from models import db, Plant

with app.app_context():
    db.drop_all()
    db.create_all()

    plants = [
        Plant(name="Aloe", image="https://example.com/aloe.jpg", price=11.50),
        Plant(name="ZZ Plant", image="https://example.com/zz-plant.jpg", price=25.98)
    ]

    db.session.add_all(plants)
    db.session.commit()
    print("Database seeded successfully!")
