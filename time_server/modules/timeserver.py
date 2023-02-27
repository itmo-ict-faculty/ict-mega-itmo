from datetime import datetime
import ntplib

class TimeServer(object):

    def __init__(self) -> None:
        pass


    @staticmethod
    async def get_time(ntp_server):
        ntp_client = ntplib.NTPClient()
        time_response = ntp_client.request(ntp_server, version=3)
        return datetime.fromtimestamp(time_response.tx_time)