"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200

## People
@app.route('/people', methods=['GET'])
def get_people():
    peoples = People.query.all()
    peoples = list(map(lambda people: people.serialize(), peoples))
    return jsonify(peoples), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id)
    people = people.serialize()
    return jsonify(people), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):

    people = People.query.get(id)
    people.delete()
    return jsonify({ "message": " PEOPLE DELETED" }), 200
## People
## PLANET
@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)
    planet.delete()
    return jsonify({ "message": "Planet DELETED" }), 200
## PLANET
## Starship
@app.route('/starships', methods=['GET'])
def get_starships():
    starshipses = Starships.query.all()
    starshipses = list(map(lambda starships: starships.serialize(), starshipses))
    return jsonify(starshipses), 200

@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starships_id(starships_id):
    starship = Starships.query.get(starships_id)
    starship = starship.serialize()
    return jsonify(starship), 200

@app.route('/starships/<int:id>', methods=['DELETE'])
def delete_starships(id):
    starship = Starships.query.get(id)
    starship.delete()
    return jsonify({ "message": "Starship DELETED" }), 200
## Starship
## ALL Favorites
@app.route('/favorite', methods=['GET'])
def get_favorite():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/favorite/<int:id>', methods=['GET'])
def select_fav(id):
    favorito = Favorite.query.filter_by(user_id = id).all()
    favorite_user = [favorite.serialize() for favorite in favorito]
    return jsonify(favorite_user), 200

@app.route('/favorite', methods=['POST'])
def new_favorite():  
    
    datos = request.get_json()
    favorite = Favorite()
    favorite.user_id = datos['user_id']
    favorite.people_id = datos['people_id']
    favorite.planet_id = datos['planet_id']
    favorite.starships_id = datos['starships_id']
    favorite.save()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people', methods=['POST'])
def new_favoritepeople(): 
    datos = request.get_json()
    favorite = Favorite()
    favorite.user_id = datos['user_id']
    favorite.people_id = datos['people_id']
    favorite.save()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet', methods=['POST'])
def new_favoriteplanet(): 
    datos = request.get_json()
    favorite = Favorite()
    favorite.user_id = datos['user_id']
    favorite.planet_id = datos['planet_id']
    favorite.save()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/starships', methods=['POST'])
def new_favoritestarships(): 
    datos = request.get_json()
    favorite = Favorite()
    favorite.user_id = datos['user_id']
    favorite.starships_id = datos['starships_id']
    favorite.save()
    return jsonify(favorite.serialize()), 201
   
@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_favoriteplanet(id):
    favorito = Favorite.query.filter_by(planet_id = id).first()
    favorito.delete()
    return jsonify({ "message": "FavPlanet DELETED" }), 200

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_favoritepeople(id):
    favorito = Favorite.query.filter_by(people_id = id).first()
    favorito.delete()
    return jsonify({ "message": "FavPeople DELETED" }), 200

@app.route('/favorite/starships/<int:id>', methods=['DELETE'])
def delete_favoritestarship(id):
    favorito = Favorite.query.filter_by(starships_id = id).first()
    favorito.delete()
    return jsonify({ "message": "FavStarship DELETED" }), 200
## ALL Favorites



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
