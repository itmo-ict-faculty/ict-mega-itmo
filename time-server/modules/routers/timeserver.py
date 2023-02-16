from fastapi import APIRouter, Depends
from loguru import logger

from ..timeserver import TimeServer

router = APIRouter()

@router.get("/get_time")
async def get_time(ntp_server: str):
    result = await TimeServer.get_time(ntp_server)
    return result