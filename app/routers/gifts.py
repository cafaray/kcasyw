from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_token_header

from typing import List
from fastapi import Body, status

from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from repository import crud, models, schemas
from repository.database import SessionLocal, engine

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()
# router = APIRouter( prefix="/draws", tags=["draws"], dependencies=[Depends(get_token_header)], responses={404: {"description": "Not found"}})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Gift])
def get_gifts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gifts = crud.get_gifts(db=db, skip=skip, limit=limit)
    return gifts

@router.post("/", response_model=schemas.Gift, status_code=201)
def create_gift(gift: schemas.GiftCreate, db: Session = Depends(get_db)):    
    gift = crud.create_gift(db=db, gift=gift)
    #print(gift)
    return gift

@router.get("/{gift-id}", response_model=schemas.Gift, status_code=200)
def get_gift(gift_id: int, db: Session = Depends(get_db)):
    gift = crud.get_gifts(db=db, gift_id=gift_id)
    if gift==None:
        error = {"code": "RESOURCE_NOT_FOUND", "message": "The gift resource doesn't exists. Verify id {}".format(gift_id) }
        json_compatible_error_data = jsonable_encoder(error)
        return JSONResponse(status_code=404, content=json_compatible_error_data)
    return gift

@router.delete("/{gift-id}", status_code=204)
def remove_gift(gift_id: int, db: Session = Depends(get_db)):
    crud.delete_gift(db=db, gift_id=gift_id)
    return Response(status_code=204)

@router.put("/{gift-id}",  status_code=200)
def update_gift(gift_id: int, gift: schemas.GiftCreate, db: Session = Depends(get_db)):
    gift = crud.update_gift(db=db, gift_id=gift_id, gift=gift)
    return gift
