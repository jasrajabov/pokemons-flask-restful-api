import os
from flask import Flask
from serializer import ma
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.pokemons import Pokemon, Pokemons
from resources.pokemon_master import PokemonMaster, PokemonsMasters, PokemonMasterById, PokemonMasterRegister, \
                            PokemonMasterLogin


app = Flask(__name__)
basdir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basdir, 'flask_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '_appsecretkey_'
app.debug = True
ma.init_app(app)

jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Pokemons, '/pokemons')
api.add_resource(Pokemon, '/pokemon/<string:master_name>/<string:name>')

api.add_resource(PokemonMaster, '/master/<string:master_name>')
api.add_resource(PokemonsMasters, '/masters')

api.add_resource(PokemonMasterById, '/master/<int:_id>')
api.add_resource(PokemonMasterRegister, '/master/register')

api.add_resource(PokemonMasterLogin, '/login')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    port = 5000
    app.run(host="0.0.0.0", port=port)
