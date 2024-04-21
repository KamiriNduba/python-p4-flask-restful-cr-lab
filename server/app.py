#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    """Class to handle requests related to multiple plants."""

    def get(self):
        """GET request to retrieve all plants."""
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)
    
    def post(self):
        """POST request to create a new plant."""
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)
    
api.add_resource(Plants,'/plants')

class PlantByID(Resource):
    """Class to handle requests related to a specific plant by ID."""
    
    def get(self, id):
        """GET request to retrieve a plant by its ID."""
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

api.add_resource(PlantByID,'/plants/<int:id>')  

if __name__ == '__main__':
    app.run(port=5555, debug=True)
