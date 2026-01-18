# server/app.py

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)

# --- Routes ---
class Home(Resource):
    def get(self):
        return make_response({"message": "Welcome to the Plant Store API"}, 200)

class PlantList(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return make_response(plant.to_dict(), 200)
        else:
            return make_response({"error": "Plant not found"}, 404)

api.add_resource(Home, '/')
api.add_resource(PlantList, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
