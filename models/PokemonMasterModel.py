from sqlalchemy import Column, Integer, String
from db import db
from hmac import compare_digest


class PokemonMasterModel(db.Model):
    __tablename__ = 'poke_masters'

    id = Column(Integer, primary_key=True)
    master_name = Column(String)
    password = Column(String)

    pokemons = db.relationship('PokemonModel', lazy='dynamic')

    def __init__(self, master_name, password):
        self.master_name = master_name
        self.password = password

    def json(self):
        return {'id': self.id, 'master_name': self.master_name, 'password': self.password,
                'pokemons': [pokemon.json() for pokemon in self.pokemons.all()]}

    def check_password(self, password):
        return compare_digest(self.password, password)

    @classmethod
    def find_pokemon_master(cls, master_name):
        pokemon = cls.query.filter_by(master_name=master_name).first()
        return pokemon

    @classmethod
    def find_by_id(cls, _id):
        pokemon = cls.query.filter_by(id=_id).first()
        return pokemon

    @classmethod
    def get_all_masters(cls):
        data = cls.query.all()
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

