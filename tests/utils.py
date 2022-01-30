import requests
from .config import LOCAL_URL
import json

class Utils:

    def post(self, data, endpoint, is_json, auth_token):
        """
        :param data: data
        :param endpoint: string
        :param json: bool
        :param auth_token: stringToken
        :return:
        """
        if auth_token:
            headers = {"Authorization": f"Bearer {auth_token}"}
            if is_json:
                json_data = json.dumps(data)
                response = requests.post(f'{LOCAL_URL}/{endpoint}', json=json_data, headers=headers)
            else:
                response = requests.post(f'{LOCAL_URL}/{endpoint}', data=data, headers=headers)
        else:
            if is_json:
                json_data = json.dumps(data)
                response = requests.post(f'{LOCAL_URL}/{endpoint}', json=json_data)
            else:
                response = requests.post(f'{LOCAL_URL}/{endpoint}', data=data)
        return response

    def get(self, id=None, endpoint=''):
        """
        :param id:
        :param endpoint:
        :return:
        """
        if id:
            response = requests.get(f'{LOCAL_URL}/{endpoint}/{id}')
        else:
            response = requests.get(f'{LOCAL_URL}/{endpoint}')
        return response

    def login(self, login_data):
        requests.post(f'{LOCAL_URL}/register', data=login_data)
        login_data_json = json.dumps({
            'email': login_data['email'],
            'password': login_data['password']
        })
        response = requests.post(f'{LOCAL_URL}/login', json=login_data_json)
        return response

    def generate_token(self, response):
        response_json = response.json()
        access_token = response_json['access_token']
        return access_token

    def search_record_by_email(self, schema, key):
        record = schema.query.filter_by(email=key).first()
        return record

    def search_record_by_data(self, schema, data):
        record = schema.query.filter_by(**data).first()
        return record

    def cleanup_db(self, db, schema, key):
        record = self.search_record_by_email(schema, key)
        db.session.delete(record)
        db.session.commit()

    def cleanup_db_by_data(self, db, schema, data):
        record = self.search_record_by_data(schema, data)
        if record:
            db.session.delete(record)
            db.session.commit()

    def add_pokemon(self, login_data, pk_data):
        response = self.login(login_data)
        access_token = self.generate_token(response)
        response = self.post(pk_data, 'add_pokemon', True, access_token)
        return response



