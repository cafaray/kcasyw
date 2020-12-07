import os, shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse

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

@router.get("/{giftid}", response_model=schemas.Gift, status_code=200)
def get_gift(giftid: int, db: Session = Depends(get_db)):
    gift = crud.get_gift(db=db, gift_id=giftid)
    if gift==None:
        error = {"code": "RESOURCE_NOT_FOUND", "message": "The gift resource doesn't exists. Verify id {}".format(giftid) }
        json_compatible_error_data = jsonable_encoder(error)
        return JSONResponse(status_code=404, content=json_compatible_error_data)
    return gift

@router.delete("/{giftid}", status_code=204)
def remove_gift(giftid: int, db: Session = Depends(get_db)):
    crud.delete_gift(db=db, gift_id=giftid)
    return Response(status_code=204)

@router.put("/{giftid}",  status_code=200)
def update_gift(giftid: int, gift: schemas.GiftCreate, db: Session = Depends(get_db)):
    gift = crud.update_gift_image(db=db, gift_id=giftid, gift=gift)
    return gift

@router.post("/{giftid}/uploadfile/")
async def create_upload_file(giftid: int, file: UploadFile = File(...), db:Session = Depends(get_db)):
    print('file received:', file.filename)
    fn = os.path.basename(file.filename)
   # open read and write the file into the server 
    open(fn, 'wb').write(file.file.read()) 
    shutil.move(fn, '../ui/static/images/{}'.format(file.filename))
    # get gift
    gift = crud.update_gift_image(db=db, gift_id=giftid, image=file.filename)    
    print('gift updated', gift)
    return {"image": file.filename}

@router.get("/{giftid}/uploadfile/")
async def get_upload_file(giftid: int, db: Session = Depends(get_db)):
    print('giftid received:', giftid)
    gift = crud.get_gift(db=db, gift_id=giftid)
    print('gift result:', gift.image)
    return FileResponse(gift.image)