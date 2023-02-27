import os

import requests as r
from fastapi import FastAPI, HTTPException, Header
from loguru import logger
from pydantic import BaseModel

import mongo

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    logger.info("Running auth server")
    if not os.getenv('TIMESERVER_URL'):
        logger.critical('No TIMESERVER_URL environment variable found')
        exit(1)
    if not os.getenv('MONGODB_CONN_STR'):
        logger.critical('No MONGODB_CONN_STR environment variable found')
        exit(1)
    logger.success('All envvars are present, server successfully started')


class Credentials(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str


class UserRetrieve(BaseModel):
    name: str
    timestamp: str
    secret: str


@app.post('/api/v1/auth-server/token', response_model=Token)
async def retrieve_auth_token(credentials: Credentials):
    if token := mongo.MongoWrapper.get_token(credentials.username, credentials.password):
        return Token(token=token)
    raise HTTPException(status_code=403, detail='Wrong username/password or user not found')


def get_time(ntp_server: str) -> str:
    resp = r.get(f"{os.getenv('TIMESERVER_URL')}/api/v1/time-server/get_time", params={'ntp_server': ntp_server})
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail='ntp server is not responding')
    if current_time := resp.json().get('time'):
        return current_time
    raise HTTPException(status_code=502, detail='No "time" field in response')


def get_svc_key(svc_token: str) -> str:
    resp = r.get(f"{os.getenv('TIMESERVER_URL')}/api/v1/service-keys/get_svckey", params={'svc_token': svc_token})
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail='Failed to encode token')
    if key := resp.json().get('key'):
        return key
    raise HTTPException(status_code=502, detail='No "key" field in response')


@app.get('/api/v1/auth-server/me', response_model=UserRetrieve)
async def get_my_data(ntp_server: str, token: str = Header(...)):
    if user := mongo.MongoWrapper.auth_user(token):
        try:
            time = get_time(ntp_server)
            key = get_svc_key(user)
            return UserRetrieve(timestamp=time, secret=key, name=user)
        except r.Timeout as e:
            raise HTTPException(status_code=502, detail='Failed to connect to time_server') from e
    raise HTTPException(status_code=403, detail='Token is not valid')
