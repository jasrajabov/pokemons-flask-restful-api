from flask import Flask, jsonify, request
import os
from models import db, User, Pokemon
from serializer import ma, pokemon_schema, pokemons_schema, user_schema, users_schema
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
import os


app = Flask(__name__)
basdir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basdir, 'flask_app.db')
app.config['JWT_SECRET_KEY'] = '_appsecretkey_'
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.debug = True

db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)

@app.cli.command(name='create_db')
def create_db():
    db.create_all()
    print('Database created!')


@app.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('seed_db')
def seed_db():
    ash = User(
        pokemon_master='Ash',
        team='Team Ash'
    )

    pikachu = Pokemon(
        pokemonname = 'Pikachu',
        pokemontype = 'Electric',
        power = 100.00,
        hp = 500.00
    )

    db.session.add(ash)
    db.session.add(pikachu)

    db.session.commit()
    print('Database seeded!')


@app.route('/pokemons', methods=['GET'])
def get_all_pokemons():
    """
    Lists all pokemons!
    :return:
    """
    pokemons = Pokemon.query.all()
    result = pokemons_schema.dump(pokemons)
    return jsonify(result), 200


#DELETE ME
@app.route('/')
def hellow():
    return jsonify(message='Hellow!!!')

@app.route('/register', methods=['POST'])
def register_master():
    """
    Handles registration of pokemon masters
    :method: POST
    :return:
    """
    email = request.form['email']
    record = User.query.filter_by(email=email).first()
    if record:
        return jsonify(message='Email exists! Try with different email!'), 409
    else:
        pokemon_master = User(
            pokemon_master=request.form['pokemon_master'],
            email=email,
            team=request.form['team'],
            password=request.form['password']

        )
        db.session.add(pokemon_master)
        db.session.commit()
        return jsonify(message='Pokemon master created successfully!'), 201

@app.route('/add_pokemon', methods=['POST'])
@jwt_required()
def add_pokemon():
    pokemonname = request.json['pokemonname']
    hp = request.json['hp']
    power = request.json['power']
    pokemon = Pokemon.query.filter_by(pokemonname=pokemonname,hp=hp, power=power).first()
    if not pokemon:
        new_pokemon = Pokemon(
            pokemonname=pokemonname,
            hp=hp,
            power=power,
            pokemontype=request.json['pokemontype']
        )
        db.session.add(new_pokemon)
        db.session.commit()
        return jsonify(message=f'{pokemonname} is successfully added!'), 200
    else:
        return jsonify(message='Such pokemon exists!'), 404

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    pokemon_master = User.query.filter_by(email=email, password=password).first()
    if pokemon_master:
        return jsonify(message='Successfully logged in!', access_token=create_access_token(identity=email)), 201
    else:
        return jsonify(message='Incorrect password or email!'), 409

@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email: str):
    res = User.query.filter_by(email=email).first()
    if res:
        msg = Message(
            f"Your password is {res.password}",
            sender='admin@pokemonapi.com',
            recipients=[email]
        )
        mail.send(msg)
        return jsonify(message=f'Password is send to {res.email}'), 201
    else:
        return jsonify(message='No email was found!'), 400


@app.route('/pokemons/<int:id>', methods=['GET'])
def get_single_pokemon(id:int):
    pokemon =  Pokemon.query.filter_by(pokemon_id=id).first()
    if pokemon:
        data = pokemon_schema.dump(pokemon)
        return jsonify(data), 200
    else:
        return jsonify(message='No pokemon was found with that id!'), 404


@app.route('/update_pokemon', methods=['PUT'])
@jwt_required()
def update_pokemon():
    data = request.json
    pokemon_id = data['pokemon_id']
    pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
    if pokemon:
        pokemon.pokemonname = data['pokemonname']
        pokemon.pokemontype = data['pokemontype']
        pokemon.power = data['power']
        pokemon.hp = data['hp']
        db.session.commit()
        return jsonify(message=f'{pokemon.pokemonname} has been updated successfully!'), 200
    else:
        return jsonify(message='No pokemon was found!'), 404


@app.route('/delete_pokemon/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pokemon(id):
    pokemon = Pokemon.query.filter_by(pokemon_id=id).first()
    if pokemon:
        db.session.delete(pokemon)
        db.session.commit()
        return jsonify(message='Pokemon has been deleted!'), 201
    else:
        return jsonify(message='No pokemon was found!'), 404

@app.route('/best_pokemons', methods=['GET'])
def get_best_pokemons():
    pokemons = Pokemon.query.order_by(Pokemon.power.desc()).limit(3)
    if pokemons:
        data = pokemons_schema.dump(pokemons)
        return jsonify(data)


if __name__ == '__main__':
    app.run()
