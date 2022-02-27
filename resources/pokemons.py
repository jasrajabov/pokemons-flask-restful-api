from models.pokemon import PokemonModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class Pokemons(Resource):
    def get(self):
        pokemons = [x.json() for x in PokemonModel.get_all_pokemons()]
        return pokemons, 200


class Pokemon(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="name is required"
                        )
    parser.add_argument('master_name',
                        type=str,
                        required=True,
                        help="master_name is required"
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="type is required"
                        )
    parser.add_argument('power',
                        type=float,
                        required=True,
                        help="power is required"
                        )
    parser.add_argument('hp',
                        type=float,
                        required=True,
                        help="hp is required"
                        )

    def get(self, name, master_name):
        pokemon = PokemonModel.query.filter_by(name=name, master_name=master_name).first()

        if pokemon:
            return pokemon.json(), 200
        else:
            return {"message": "No pokemon was found with that name and team"}, 404

    @jwt_required()
    def post(self, name, master_name):
        pokemon = PokemonModel.find_pokemon(name, master_name)
        if not pokemon:
            data = Pokemon.parser.parse_args()
            new_pokemon = PokemonModel(**data)
            new_pokemon.save_to_db()
            return {"message": "Pokemon has been added successfully!", "data": new_pokemon.json()}, 200
        else:
            return {"message": "Such pokemon exists!"}, 404

    @jwt_required()
    def put(self, name, master_name):
        data = Pokemon.parser.parse_args()
        pokemon = PokemonModel.find_pokemon(name, master_name)
        if pokemon:
            pokemon.hp = data['hp']
            pokemon.power = data['power']
            pokemon.save_to_db()
            return {"message": "Pokemon has been updated successfully!", "data": pokemon.json()}, 201
        else:
            pokemon = PokemonModel(**data)
            pokemon.save_to_db()
            return {"message": "Pokemon has been added successfully!", "data": pokemon.json()}, 200

    @jwt_required()
    def delete(self, name, master_name):
        pokemon = PokemonModel.find_pokemon(name, master_name)
        if pokemon:
            pokemon.delete_from_db()
            return {"message": "Pokemon has been deleted successfully!", "data": pokemon.json()}, 200
        else:
            return {"message": "No pokemon was found with that name and team"}, 404
