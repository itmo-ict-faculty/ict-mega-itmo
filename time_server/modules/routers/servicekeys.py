from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..servicekeys import ServiceKeys


router = APIRouter()

class ServiceKeyRetrieve(BaseModel):
    key: str

@router.get("/get_svckey", response_model=ServiceKeyRetrieve)
async def get_time(svc_token: str):
    return ServiceKeyRetrieve(key=await ServiceKeys.get_svckey(svc_token))