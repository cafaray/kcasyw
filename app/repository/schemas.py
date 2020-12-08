from pydantic import BaseModel, Field
from typing import List, Optional
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

class ParticipantList(BaseModel):
    participants: List[ParticipantLink]
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

class GiftList(BaseModel):
    gifts: List[GiftLink]


class Gift(GiftBase):
    id: int
    gift: str
    quantity: Optional[int]
    description: str
    image: str
    group: Group
    class Config:
        orm_mode=True


class DrawParticipants(BaseModel):
    draw: Optional[Draw]
    participants: Optional[List[Participant]]
    class Config:
        orm_mode=True

class DrawParticipantsCreate(BaseModel):
    iddraw: Optional[DrawLink]= Field(
        None, title="The draw identificator is informed for the operation inside the path param."
    )
    idparticipant: ParticipantLink

#class DrawGiftsBase(BaseModel):
#    iddraw: DrawLink
#    idgift: GiftLink

class DrawGiftCreate(BaseModel):
    iddraw: Optional[DrawLink]= Field(
        None, title="The draw identificator is informed for the operation inside the path param."
    )
    gifts: GiftLink

class DrawGifts(BaseModel):
    draw: Optional[Draw]
    gifts: Optional[List[Gift]]
    class Config:
        orm_mode=True

class DrawParticipantGift(BaseModel):
    id: int
    draw: Draw = 1
    participant: Participant = 1
    gift: Gift = 1
    dtselection: date
    dtmail: date

class DrawParticipantGiftCreate(BaseModel):
    draw: Optional[DrawLink] = Field(
        None, title="The draw identificator is informed for the operation inside the path param."
    )
    participant: ParticipantLink
    gift: GiftLink
    dateselection: date

class DrawPublishBase(BaseModel):
    startDate: date    
    endDate: Optional[date]
    access_code: str

class DrawPublishCreate(DrawPublishBase):
    pass

class DrawPublish(DrawPublishBase):
    draw: Draw
    startDate: date    
    endDate: Optional[date]
    access_code: str
    class Config:
        orm_mode=True

class DrawEndPublish(BaseModel):
    enddate: date

class DrawGiftAvailable(BaseModel):
    iddraw: int
    idgroup: int
    alias: str

class DrawGiftsAvailable(BaseModel):
    gifts: List[DrawGiftAvailable]