from src.jwt_handler import create_JWT_for_tests
from tests.conftest import client


def test_valid_token():
    token = create_JWT_for_tests('KUmBuTer', 120)
    response = client.get('/user/salary_info', params={
        'token': token
    })
    assert response.json() == {'data':
                                   {'greeting': 'Hello, Fuijisawa Bevis!',
                                    'your_date_of_next_increase': '2024-01-08',
                                    'your_salary': 34782}}


def test_invalid_token():
    response = client.get('/user/salary_info', params={
        'token': 'very-very valid token'
    })
    assert response.json() == {'error': 'Invalid or Expired Token!'}


def test_expired_token():
    token = create_JWT_for_tests('KUmBuTer', 0)
    response = client.get('/user/salary_info', params={
        'token': token
    })
    assert response.json() == {'error': 'Invalid or Expired Token!'}
