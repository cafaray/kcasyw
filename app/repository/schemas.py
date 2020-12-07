from pydantic import BaseModel
from typing import List
from datetime import date

class DrawBase(BaseModel):
    title: str
    fordate: date

class DrawCreate(DrawBase):
    pass

class Draw(DrawBase):
    id: int
    title: str
    fordate: date
    status: str
    class Config:
        orm_mode = True

class DrawLink(BaseModel):
    id: int

class GroupBase(BaseModel):
    groupname: str
    description: str

class GroupLink(BaseModel):
    id: int

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int
    groupname: str
    description: str
    class Config:
        orm_mode = True

class ParticipantBase(BaseModel):    
    participant: str
    email: str
    group: GroupLink

class ParticipantLink(BaseModel):
    id: int

class ParticipantCreate(ParticipantBase):
    pass 

class Participant(ParticipantBase):
    id: int
    participant: str
    email: str
    group: Group
    class Config:
        orm_mode = True

class GiftBase(BaseModel):
    gift: str
    quantity: int
    description: str
    image: str
    group: GroupLink

class GiftLink(BaseModel):
    id: int

class GiftCreate(GiftBase):
    pass

class Gift(GiftBase):
    id: int

class DrawParticipantsBase(BaseModel):
    iddraw: DrawLink
    idparticipant: ParticipantLink

class DrawParticipantsCreate(DrawParticipantsBase):
    pass

class DrawParticipants(BaseModel):
    draw: Draw = -1
    participants: List[Participant] = []

class DrawGiftsBase(BaseModel):
    iddraw: DrawLink
    idgift: GiftLink

class DrawGiftCreate(DrawGiftsBase):
    pass

class DrawGifts(BaseModel):
    draw: Draw = -1
    gifts: List[Gift] = []

class DrawParticipantGift(BaseModel):
    id: int
    draw: Draw = 1
    participant: Participant = 1
    gift: Gift = 1
    dtselection: date
    dtmail: date

class DrawParticipantGiftCreate(BaseModel):
    draw: DrawLink
    participant: ParticipantLink
    gift: GiftLink
    dateselection: date