from fastapi import FastAPI, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import UserLogin
from jwt_handler import sign_JWT, decode_JWT
from database import get_async_session, User

import bcrypt

app = FastAPI(
    title='REST-service'
)


async def check_if_password_is_valid(entered_password: str, hashed_password: str):
    return bcrypt.checkpw(entered_password.encode(), hashed_password.encode())


@app.post('/user/login', tags=['user'])
async def user_login(user_schema: UserLogin, session: AsyncSession = Depends(get_async_session)):
    query = select(User.hashed_password).where(User.login == user_schema.login)
    result = (await session.execute(query)).all()
    if not result:
        return {'error': 'Invalid login!'}
    else:
        result = result[0][0]
        if await check_if_password_is_valid(user_schema.password, result):
            return sign_JWT(user_schema.login)
        else:
            return {'error': 'Invalid password!'}


@app.get('/user/salary_info', tags=["salary information"])
async def get_salary_info(token: str, session: AsyncSession = Depends(get_async_session)):
    payload = decode_JWT(token)
    if payload:
        login = payload['user_login']
        query = select(User.salary, User.date_of_next_increase, User.name, User.surname).where(User.login == login)
        salary, date, name, surname = (await session.execute(query)).all()[0]
        return {'data': {
            'greeting': f'Hello, {surname} {name}!',
            'your_salary': salary,
            'your_date_of_next_increase': date if date is not None else 'Unknown date'
        }}
    else:
        return {'error': 'Invalid or Expired Token!'}
