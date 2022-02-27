from sqlalchemy import Column, Integer, String, Float
from db import db


class PokemonModel(db.Model):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    master_name = Column(String, db.ForeignKey('poke_masters.master_name'))
    name = Column(String)
    type = Column(String)
    power = Column(Float)
    hp = Column(Float)

    master = db.relationship('PokemonMasterModel')

    def __init__(self, master_name, name, type, power, hp):
        self.master_name = master_name
        self.name = name
        self.type = type
        self.power = power
        self.hp = hp

    def json(self):
        return {'master_name': self.master_name,
                'name': self.name,
                'hp': self.hp,
                'power': self.power,
                'type': self.type}

    @classmethod
    def find_pokemon(cls, name, master_name):
        pokemon = cls.query.filter_by(name=name, master_name=master_name).first()
        return pokemon

    @classmethod
    def get_all_pokemons(cls):
        data = cls.query.all()
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()