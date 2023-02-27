from fastapi import FastAPI
from loguru import logger

from modules.routers import timeserver, servicekeys

api = FastAPI()


@api.on_event("startup")
def startup() -> None:
    logger.info("Running time server")


api.include_router(timeserver.router, prefix="/api/v1/time-server", tags=["Time Server"])
api.include_router(servicekeys.router, prefix="/api/v1/service-keys", tags=["Service Keys"])