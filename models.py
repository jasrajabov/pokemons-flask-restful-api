from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'poke_masters'
    user_id = Column(Integer, primary_key=True)
    pokemon_master = Column(String)
    email = Column(String)
    password = Column(String)
    team = Column(String)


class Pokemon(db.Model):
    __tablename__ = 'pokemons'
    pokemon_id = Column(Integer, primary_key=True)
    pokemonname = Column(String)
    pokemontype = Column(String)
    power = Column(Float)
    hp = Column(Float)


