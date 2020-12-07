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

@router.get("/", response_model=List[schemas.Draw])
def get_draws(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    draws = crud.get_draws(db=db, skip=skip, limit=limit)
    return draws

@router.post("/", response_model=schemas.Draw, status_code=201)
def create_draw(draw: schemas.DrawCreate, db: Session = Depends(get_db)):    
    draw = crud.create_draw(db=db, draw=draw)
    return draw

@router.get("/{drawid}", response_model=schemas.Draw, status_code=200)
def get_draw(drawid: int, db: Session = Depends(get_db)):
    draw = crud.get_draw(db=db, draw_id=drawid)
    if draw==None:
        error = {"code": "RESOURCE_NOT_FOUND", "message": "The draw resource doesn't exists. Verify id {}".format(drawid) }
        json_compatible_error_data = jsonable_encoder(error)
        return JSONResponse(status_code=404, content=json_compatible_error_data)
    return draw

@router.delete("/{drawid}", status_code=204)
def remove_draw(drawid: int, db: Session = Depends(get_db)):
    crud.delete_draw(db=db, draw_id=drawid)
    return Response(status_code=204)

@router.put("/{drawid}",  status_code=200)
def update_draw(drawid: int, draw: schemas.DrawCreate, db: Session = Depends(get_db)):
    draw = crud.update_draw(db=db, draw_id=drawid, draw=draw)
    return draw

# draw-participants operations:
#@router.post("/{drawid}/participants", status_code=201)
#def post_draw_participant(drawid: int, participants: schemas.ParticipantList, db: Session = Depends(get_db)):
#    draw_participant = crud.add_draw_participant(db=db, draw_id=drawid, participant_id=participant.id)
#    return draw_participant

@router.post("/{drawid}/participants", status_code=201)
def post_draw_participants(drawid: int, participants: schemas.ParticipantList, db: Session = Depends(get_db)):
    draw_participant = crud.add_draw_participants(db=db, draw_id=drawid, participants=participants)
    return draw_participant

@router.get("/{drawid}/participants", response_model=schemas.DrawParticipants, status_code=200)
def get_draw_participants(drawid: int, db: Session = Depends(get_db)):
    drawParticipants = crud.get_draw_participants(db=db, draw_id=drawid)
    return drawParticipants

@router.post("/{drawid}/gifts", status_code=201)
def post_draw_gifts(drawid: int, gifts: schemas.GiftList, db: Session = Depends(get_db)):
    draw_gift = crud.add_draw_gifts(db=db, draw_id=drawid, gifts=gifts)
    return draw_gift

#@router.post("/{drawid}/bulk-gifts", status_code=201)
#def post_draw_gifts(drawid: int, gifts: schemas.GiftList, db: Session = Depends(get_db)):
#    draw_gift = crud.add_draw_gifts(db=db, draw_id=drawid, gifts=gifts)
#    return draw_gift

@router.get("/{drawid}/gifts", response_model=schemas.DrawGifts, status_code=200)
def get_draw_gifts(drawid: int, db: Session = Depends(get_db)):
    draw_gifts = crud.get_draw_gifts(db=db, draw_id=drawid)
    return draw_gifts

@router.get("/{drawid}/selections", response_model=schemas.DrawParticipantGift, status_code=200)
def get_draw_participants_gifts(drawid: int, db: Session = Depends(get_db)):
    draw_gifts = crud.get_draw_participants_gifts(db=db, draw_id=drawid)
    return draw_gifts

@router.post("/{drawid}/selections", status_code=201)
def post_draw_participant_gift(drawid: int, draw_participant_gift: schemas.DrawParticipantGiftCreate, db: Session = Depends(get_db)):    
    draw_participant_gift = crud.add_draw_participant_gift(db=db, draw_id=drawid, draw_participant_gift=draw_participant_gift)
    return draw_participant_gift

#@router.delete("/{draw-id}/participants/{participant-id}", status_code=204)
#def delete_draw_participants(draw_id: int, participant_id: int, db: Session = Depends(get_db)):
#    crud.delete_draw_participant(db=db, draw_id=draw_id, participant_id=participant_id)
#    return Response(status_code=204)


#class DrawState(str, Enum):
#    pending = "pending"
#    onlive = "onlive"
#    done = "done"

#class Draw(BaseModel):
#    id: int = Field(
#        None, title="Unique identifier for a draw."
#    )
#    title: str = Field(
#        None, title="Title for the event draw", max_length=100
#    )
#    dateat: str = Field(
#        None, title="Date for the event draw", max_length=10
#    )    
#    status: DrawState = Field(
#        None, title="State of the draw, could it be pending, onlive, or done."
#    )    
#    class Config:
#        schema_extra = {
#            "example": {
#                "title": "Navidad 2020", 
#                "dateat": "2020-12-17"
#            }
#        }


#fake_draws_db = [
#    {"id": 1, "title": "Navidad 2020", "dateat": "2020-12-17", "status":"pending"}, 
#    {"id": 2, "title": "Aniversario 2021", "dateat": "2021-03-07", "status":"pending"}, 
#    {"id": 3, "title": "Día del enzima", "dateat": "2021-05-10", "status":"pending"}
#]
