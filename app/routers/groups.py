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
# router = APIRouter(prefix="/draws", tags=["draws"], dependencies=[Depends(get_token_header)], responses={404: {"description": "Not found"}})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Group], summary="Get all groups")
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all the groups from repository:

    - **skip**: offset to start the results
    - **limit**: an integer wich represents the number of values to include in the response
    \f
    :param skip: User input.
    :param limit: User input.
    """
    groups = crud.get_groups(db=db, skip=skip, limit=limit)
    return groups

@router.post("/", response_model=schemas.Group, status_code=201)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):    
    group = crud.create_group(db=db, group=group)
    return group

@router.get("/{groupid}", response_model=schemas.Group, status_code=200)
def get_group(groupid: int, db: Session = Depends(get_db)):
    group = crud.get_group(db=db, group_id=groupid)
    if group==None:
        error = {"code": "RESOURCE_NOT_FOUND", "message": "The group resource doesn't exists. Verify id {}".format(groupid) }
        json_compatible_error_data = jsonable_encoder(error)
        return JSONResponse(status_code=404, content=json_compatible_error_data)
    return group

@router.delete("/{groupid}", status_code=204)
def remove_group(groupid: int, db: Session = Depends(get_db)):
    crud.delete_group(db=db, group_id=groupid)
    return Response(status_code=204)

@router.put("/{groupid}",  status_code=200)
def update_group(groupid: int, group: schemas.GroupCreate, db: Session = Depends(get_db)):
    group = crud.update_group(db=db, group_id=groupid, group=group)
    return group
