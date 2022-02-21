from models.PokemonMasterModel import PokemonMasterModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required


class PokemonsMasters(Resource):
    def get(self):
        pokemons = [x.json() for x in PokemonMasterModel.get_all_masters()]
        return pokemons, 200


class PokemonMaster(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('master_name',
                        type=str,
                        required=True,
                        help="master_name is required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password is required")

    def get(self, master_name):
        master = PokemonMasterModel.find_pokemon_master(master_name)
        if master:
            return master.json(), 200
        else:
            return {"message": "Pokemon master was not found!"}, 404


    def post(self, master_name):
        master = PokemonMasterModel.find_pokemon_master(master_name)
        if not master:
            data = PokemonMaster.parser.parse_args()
            master = PokemonMasterModel(**data)
            master.save_to_db()
            return {"message": "Pokemon master has been added successfully!", "data": master.json()}, 200
        else:
            return {"message": "Pokemon master exists with that name!"}, 400


class PokemonMasterById(Resource):

    def get(self, _id):
        master = PokemonMasterModel.find_by_id(_id)
        if master:
            return master.json(), 200
        else:
            return {"message": "Pokemon master was not found!"}, 404


class PokemonMasterRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('master_name',
                        type=str,
                        required=True,
                        help="master_name is required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password is required")

    def post(self):
        data = PokemonMaster.parser.parse_args()
        master = PokemonMasterModel.find_pokemon_master(data['master_name'])
        if not master:
            master = PokemonMasterModel(**data)
            master.save_to_db()
            return {"message": "Pokemon master has been added successfully!", "data": master.json()}, 200
        else:
            return {"message": "Pokemon master exists with that name!"}, 400



class PokemonMasterLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('master_name',
                        type=str,
                        required=True,
                        help="master_name is required"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password is required")

    def post(self):
        data = PokemonMaster.parser.parse_args()
        pokemon_master = PokemonMasterModel.find_pokemon_master(data['master_name'])
        if pokemon_master and pokemon_master.check_password(data['password']):
            access_token = create_access_token(identity=pokemon_master.json())

            return {"access_token": access_token}
