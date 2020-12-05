from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum, PrimaryKeyConstraint, Table, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from .database import Base

class DrawParticipants(Base):
    __tablename__ = "kmgm01t"
    iddraw = Column(Integer, ForeignKey("kmgm00t.id"), primary_key=True)
    idparticipant = Column(Integer, ForeignKey("kmgm11t.id"), primary_key=True)

class DrawGifts(Base):
    __tablename__ = "kmgm02t"
    iddraw = Column(Integer, ForeignKey("kmgm00t.id"), primary_key=True)
    idgift = Column(Integer, ForeignKey("kmgm12t.id"), primary_key=True)

class Draw(Base):
    __tablename__ = "kmgm00t"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    fordate = Column(Date())
    status = Column(Enum('pending','onlive','closed'))

    participants = relationship("Participant", secondary='kmgm01t', back_populates="draws")
    gifts = relationship("Gifts", secondary='kmgm02t', back_populates="draws")
    
    drawpart = relationship("Participant", secondary='kmgm20t')

class Group(Base):
    __tablename__ = "kmgm10t"
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String, unique=True, index=True)
    description = Column(String)

    participants = relationship("Participant", back_populates="group")
    gifts = relationship("Gifts", back_populates="group")

class Participant(Base):
    __tablename__ = "kmgm11t"
    id = Column(Integer, primary_key=True, index=True)
    participant = Column(String)
    email = Column(String, unique=True, index=True)
    idgroup = Column(Integer, ForeignKey("kmgm10t.id"))

    group = relationship("Group", back_populates="participants")
    draws = relationship("Draw", secondary='kmgm01t', back_populates="participants")
    
    drawgift = relationship("Gifts", secondary="kmgm20t")

class Gifts(Base):
    __tablename__ = "kmgm12t"
    id = Column(Integer, primary_key=True, index=True)
    gift = Column(String)
    quantity = Column(String, unique=True, index=True)
    description = Column(String)
    image = Column(String)
    idgroup = Column(Integer, ForeignKey("kmgm10t.id"))

    group = relationship("Group", back_populates="gifts")
    draws = relationship("Draw", secondary='kmgm02t', back_populates="gifts")

    drawselect = relationship("Participant", secondary="kmgm20t")

class DrawParticipantGift(Base):
    __tablename__="kmgm20t"
    id = Column(Integer, primary_key=True, index=True)
    iddraw = Column(Integer, ForeignKey('kmgm00t.id'), primary_key=True)
    idparticipant = Column(Integer, ForeignKey('kmgm11t.id'), primary_key=True)
    idgift = Column(Integer, ForeignKey('kmgm12t.id'), primary_key=True)
    dateselection = Column(Date())
    datemail = Column(Date())