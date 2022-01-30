from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'pokemon_master', 'email', 'password', 'team')


class PokemonSchema(ma.Schema):
    class Meta:
        fields = ('pokemon_id', 'pokemonname', 'pokemontype', 'power', 'hp')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

pokemon_schema = PokemonSchema()
pokemons_schema = PokemonSchema(many=True)