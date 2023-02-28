import os

from pymongo import MongoClient


class _Mongo:
    def __init__(self):
        conn_str = os.getenv('MONGODB_CONN_STR')
        if not conn_str:
            raise IOError('MONGODB_CONN_STR not specified')
        mongo_client_url = str(conn_str)
        self.mongo: MongoClient = MongoClient(mongo_client_url)
        self._db = self.mongo['auth']
        self._users_collection = self._db['users']

    def get_token(self, username: str, password: str) -> str | None:
        user = self._users_collection.find_one({'username': username, 'password': password})
        return f"{username}_{password}" if user else None

    def auth_user(self, token: str) -> str | None:
        data = token.split('_')
        if len(data) != 2:
            return None
        user = self._users_collection.find_one({'username': data[0], 'password': data[1]})
        return user['full_name'] if user else None


MongoWrapper = _Mongo()
