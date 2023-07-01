from tests.conftest import client


def test_correct_data():
    response = client.post('/user/login', json={
        "login": "KUmBuTer",
        "password": "7j8QV39dv*g0"
    })
    assert list(response.json().keys())[0] == 'access token'


def test_invalid_password():
    response = client.post('/user/login', json={
        "login": "KUmBuTer",
        "password": "string"
    })
    assert response.json() == {'error': 'Invalid password!'}


def test_login_does_not_exist():
    response = client.post('/user/login', json={
        "login": "string",
        "password": "string"
    })
    assert response.json() == {'error': 'Invalid login!'}