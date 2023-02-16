from fastapi import APIRouter, Depends
from loguru import logger

from ..servicekeys import ServiceKeys


router = APIRouter()

@router.get("/get_svckey")
async def get_time(svc_token: str):
    result = await ServiceKeys.get_svckey(svc_token)
    return result