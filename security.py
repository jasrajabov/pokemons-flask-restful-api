from hmac import compare_digest
from models.PokemonMasterModel import PokemonMasterModel


def authenticate(master_name, password):
    pokemon_master = PokemonMasterModel.find_pokemon_master(master_name)
    if pokemon_master and compare_digest(pokemon_master.password.encode('utf-8'), password.encode('utf-8')):
        return pokemon_master


def identity(payload):
    master_id = payload['identity']
    return PokemonMasterModel.find_by_id(master_id)
