<<<<<<< HEAD
# biocera-backend/promotion_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter(prefix="/promotion", tags=["promotion"])

class Promotion(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None = None
    start_date: date
    end_date: date

_fake_db: List[Promotion] = []

@router.post("/", response_model=Promotion)
def create_promotion(p: Promotion):
    _fake_db.append(p)
    return p

@router.get("/latest", response_model=List[Promotion])
def list_promotions():
    return _fake_db[-10:]
=======
# biocera-backend/promotion_api.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from typing import List

router = APIRouter(prefix="/promotion", tags=["promotion"])

class Promotion(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None = None
    start_date: date
    end_date: date

_fake_db: List[Promotion] = []

@router.post("/", response_model=Promotion)
def create_promotion(p: Promotion):
    _fake_db.append(p)
    return p

@router.get("/latest", response_model=List[Promotion])
def list_promotions():
    return _fake_db[-10:]
>>>>>>> bd2cffc42140f854728f5a0635c312437dafb511
