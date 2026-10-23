from fastapi import APIRouter, HTTPException, status

from app.models import Cryptid
from app.schemas import CryptidOut

router = APIRouter(prefix="/api")


@router.get("/cryptids", response_model=list[CryptidOut])
async def list_cryptids() -> list[Cryptid]:
    return await Cryptid.find_all().sort(Cryptid.code).to_list()


@router.get("/cryptids/{code}", response_model=CryptidOut)
async def get_cryptid(code: str) -> Cryptid:
    cryptid = await Cryptid.find_one(Cryptid.code == code.upper())
    if cryptid is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such case file")
    return cryptid
