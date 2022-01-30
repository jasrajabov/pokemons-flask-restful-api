import pytest
from app import app
import subprocess, signal
import os
import time
from .utils import Utils
import random

@pytest.fixture
def pk_master_data():
    data = {
            'pokemon_master': 'test_master',
            'email': f'test_email_{random.randint(1,100)}@test.com',
            'team': f'test_team_{random.randint(1,100)}',
            'password': 'test_password1'
        }
    return data


@pytest.fixture
def pk_data():
    data = {
            'pokemonname': 'Onyxx',
            'pokemontype': 'Rock',
            'power': random.randint(0, 100),
            'hp': random.randint(0, 100)
        }
    return data


@pytest.fixture
def login_data():
    data = {
        'pokemon_master': 'test_master',
        'email': 'forlogin_test@test.com',
        'team': 'test_team_1',
        'password': 'test_password1'
    }
    return data


@pytest.fixture
def ut():
    return Utils()


@pytest.fixture(scope="session")
def _app():
    app.app_context().push()


@pytest.fixture(scope="session")
def run_test_serv(_app):
    sp = subprocess.Popen("python ../app.py", shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    time.sleep(2)
    yield
    print('Shutting down local server...')
    os.kill(os.getpgid(sp.pid), signal.SIGTERM)




