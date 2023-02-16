from datetime import datetime
from loguru import logger
import asyncio
import os 
import ntplib

class TimeServer(object):

    def __init__(self) -> None:
        pass


    async def get_time(ntp_server):
        ntp_client = ntplib.NTPClient()
        time_response = ntp_client.request(ntp_server, version=3)
        time_response.offset
        result = datetime.fromtimestamp(time_response.tx_time)
        return result