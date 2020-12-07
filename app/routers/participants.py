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

@router.get("/", response_model=List[schemas.Participant])
def get_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    participants = crud.get_participants(db=db, skip=skip, limit=limit)
    return participants

@router.post("/", response_model=schemas.Participant, status_code=201)
def create_participant(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):    
    participant = crud.create_participant(db=db, participant=participant)
    return participant

@router.get("/{participantid}", response_model=schemas.Participant, status_code=200)
def get_participant(participantid: int, db: Session = Depends(get_db)):
    participant = crud.get_participant(db=db, participant_id=participantid)
    if participant==None:
        error = {"code": "RESOURCE_NOT_FOUND", "message": "The participant resource doesn't exists. Verify id {}".format(participantid) }
        json_compatible_error_data = jsonable_encoder(error)
        return JSONResponse(status_code=404, content=json_compatible_error_data)
    return participant

@router.delete("/{participantid}", status_code=204)
def remove_participant(participantid: int, db: Session = Depends(get_db)):
    crud.delete_participant(db=db, participant_id=participantid)
    return Response(status_code=204)

@router.put("/{participantid}",  status_code=200)
def update_participant(participantid: int, participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    participant = crud.update_participant(db=db, participant_id=participantid, participant=participant)
    return participant
