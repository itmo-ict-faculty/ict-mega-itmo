from datetime import datetime
from loguru import logger
import base64
import asyncio
import os 


class ServiceKeys(object):

    def __init__(self) -> None:
        pass


    async def get_svckey(svc_token):
        svc_token = svc_token.encode("ascii")
        result = base64.b64encode(svc_token)
        return result