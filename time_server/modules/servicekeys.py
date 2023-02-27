import base64

class ServiceKeys(object):

    def __init__(self) -> None:
        pass


    @staticmethod
    async def get_svckey(svc_token):
        svc_token = svc_token.encode("ascii")
        return base64.b64encode(svc_token)