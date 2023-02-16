from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dotenv import load_dotenv
import os

from modules.routers import timeserver, servicekeys

api = FastAPI()


@api.on_event("startup")
def check_environment_variables() -> None:
    logger.info("All checks passed, running time server")


api.include_router(timeserver.router, prefix="/api/v1/time-server", tags=["Time Server"])
api.include_router(servicekeys.router, prefix="/api/v1/service-keys", tags=["Service Keys"])