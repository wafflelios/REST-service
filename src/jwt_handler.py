import time
import jwt
from decouple import config

# Здесь происходит работа с JWT(JSON Web Tokens), который будет выдаваться пользователю после авторизации для просмотра
# Своей заработной платы и даты следующего повышения

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')


# Просто вывод токена для пользователя
def token_response(token: str):
    return {"access token": token}


# "Генерация" токена для авторизированного пользователя
# Токен будет валидным в течение 120 секунд, то есть двух минут
def sign_JWT(user_login: str):
    payload = {
        "user_login": user_login,
        "expiry": time.time() + 120
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


# Возвращает декодированный токен, если он валидный
def decode_JWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expiry'] >= time.time() else None
    except:
        return {}


def create_JWT_for_tests(user_login: str, seconds: int):
    payload = {
        "user_login": user_login,
        "expiry": time.time() + seconds
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
