from assertpy import assert_that
from models import db, User, Pokemon
import json


class TestEndpoints:

    def test_home_page(self, run_test_serv, ut):
        response = ut.get()
        response_json = response.json()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response_json['message']).is_equal_to('Pokemon API Homepage!')

    def test_register_pokemon_master(self, ut, pk_master_data):
        response = ut.post(pk_master_data, 'register', False, '')
        response_json = response.json()
        assert_that(response_json['message']).is_equal_to('Pokemon master created successfully!')
        ut.cleanup_db(db, User, pk_master_data['email'])
        pokemon_master_db = ut.search_record_by_email(User, pk_master_data['email'])
        assert_that(pokemon_master_db).is_none()

    def test_existing_email(self, ut, pk_master_data):
        response_1 = ut.post(pk_master_data, 'register', False, '')
        response_json_1 = response_1.json()
        assert_that(response_json_1['message']).is_equal_to('Pokemon master created successfully!')
        response_2 = ut.post(pk_master_data, 'register', False, '')
        response_json_2 = response_2.json()
        assert_that(response_json_2['message']).is_equal_to('Email exists! Try with different email!')
        ut.cleanup_db(db, User, pk_master_data['email'])

    def test_delete_pokemon_master_without_auth_fails(self, ut, pk_master_data):
        response_1 = ut.post(pk_master_data, 'register', False, '')
        response_1_js = response_1.json()
        assert_that(response_1_js['message']).is_equal_to('Pokemon master created successfully!')
        response_2 = ut.post(pk_master_data, 'delete_pokemon_master', True, '')
        assert_that(response_2.status_code).is_equal_to(401)
        assert_that(response_2.json()['msg']).contains('Missing Authorization Header')
        ut.cleanup_db(db, User, pk_master_data['email'])

    def test_create_pokemon_without_auth_fails(self, ut, pk_data):
        response = ut.post(pk_data, 'add_pokemon', True, '')
        assert_that(response.status_code).is_equal_to(401)
        assert_that(response.json()['msg']).contains('Missing Authorization Header')

    def test_login(self, ut, pk_master_data, login_data):
        response = ut.login(login_data)
        response_json = response.json()
        assert_that(response_json['message']).contains('Success')
        access_token = ut.generate_token(response)
        response_1 = ut.post(pk_master_data, 'register', False, access_token)
        response_json = response_1.json()
        assert_that(response_json['message']).is_equal_to('Pokemon master created successfully!')
        response_2 = ut.post(pk_master_data, 'delete_pokemon_master', True, access_token)
        assert_that(response_2.status_code).is_equal_to(202)
        assert_that(response_2.json()['message']).contains('has been deleted successfully!')

    def test_add_pokemon_with_auth(self, ut, login_data, pk_data):
        response = ut.add_pokemon(login_data, pk_data)
        assert_that(response.status_code).is_equal_to(200)
        ut.cleanup_db_by_data(db, Pokemon, pk_data)

    def test_get_pokemon_by_id(self, ut, login_data, pk_data):
        ut.add_pokemon(login_data, pk_data)
        db_data = ut.search_record_by_data(Pokemon, pk_data)
        pk_id = db_data.pokemon_id
        response = ut.get(id=pk_id, endpoint='pokemons')
        response_json = response.json()
        assert_that(response_json['pokemonname']).is_equal_to(pk_data['pokemonname'])
        assert_that(response_json['pokemontype']).is_equal_to(pk_data['pokemontype'])
        assert_that(response_json['power']).is_equal_to(pk_data['power'])
        assert_that(response_json['hp']).is_equal_to(pk_data['hp'])
        ut.cleanup_db_by_data(db, Pokemon, pk_data)










