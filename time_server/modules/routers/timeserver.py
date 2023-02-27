import socket
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..timeserver import TimeServer

router = APIRouter()

class TimeRetrieve(BaseModel):
    time: str | datetime


@router.get("/get_time", response_model=TimeRetrieve)
async def get_time(ntp_server: str):
    try:
        return TimeRetrieve(time=await TimeServer.get_time(ntp_server))
    except socket.gaierror:
        raise HTTPException(status_code=500, detail='Wrong ntp_server')
    except:
        raise HTTPException(status_code=500, detail='Unhandled exception')