from sqlalchemy.orm import Session

from . import models, schemas

def get_draw(db: Session, draw_id: int):
    return db.query(models.Draw).filter(models.Draw.id == draw_id).first()

def get_draws(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Draw).offset(skip).limit(limit).all()

def create_draw(db: Session, draw: schemas.DrawCreate):
    #fake_hashed_password = user.password + "notreallyhashed"
    db_draw = models.Draw(title=draw.title, fordate=draw.fordate, status='pending')
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw

def update_draw(db: Session, draw_id: int, draw: schemas.DrawCreate):
    new_draw = db.query(models.Draw).filter(models.Draw.id == draw_id).update({ "title":draw.title, "fordate":draw.fordate })    
    if new_draw == None:
        return None
    db.commit()
    return get_draw(db, draw_id)

def delete_draw(db: Session, draw_id: int):    
    draw = get_draw(db, draw_id)
    db.delete(draw)
    db.commit()
    return -1

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(groupname=group.groupname, description=group.description)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group: schemas.GroupCreate):
    r = db.query(models.Group).filter(models.Group.id == group_id).update({ "groupname": group.groupname, "description": group.description })
    if r == None:
        return None
    db.commit()
    new_group = get_group(db, group_id)
    return new_group

def delete_group(db: Session, group_id: int):
    db_group = get_group(db, group_id)
    db.delete(db_group)
    db.commit()
    return -1

def get_participant(db: Session, participant_id: int):
    return db.query(models.Participant).join(models.Group, models.Group.id == models.Participant.idgroup).filter(models.Participant.id == participant_id).first()

def get_participants(db: Session, skip: int = 0, limit: int = 100):
    participants = db.query(models.Participant).join(models.Group, models.Group.id == models.Participant.idgroup).offset(skip).limit(limit).all()
    return participants

def create_participant(db: Session, participant: schemas.ParticipantCreate):
    db_participant = models.Participant(participant=participant.participant, email=participant.email, idgroup=participant.group.id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def update_participant(db: Session, participant_id: int, participant: schemas.ParticipantCreate):
    r = db.query(models.Participant).filter(models.Participant.id == participant_id).update({ "participant": participant.participant, "email": participant.email, "idgroup": participant.group.id })
    if r == None:
        return None
    db.commit()
    new_participant = get_participant(db, participant_id)
    return new_participant

def delete_participant(db: Session, participant_id: int):
    db_participant = get_participant(db, participant_id)
    db.delete(db_participant)
    db.commit()
    return -1

def get_gift(db: Session, gift_id: int):
    return db.query(models.Gifts).join(models.Group, models.Group.id == models.Gifts.idgroup).filter(models.Gifts.id == gift_id).first()

def get_gifts(db: Session, skip: int = 0, limit: int = 100):
    gifts = db.query(models.Gifts).join(models.Group, models.Group.id == models.Gifts.idgroup).offset(skip).limit(limit).all()
    return gifts

def create_gift(db: Session, gift: schemas.GiftCreate):
    db_gift = models.Gifts(gift =gift.gift, quantity=gift.quantity, description=gift.description, image=gift.image,  idgroup=gift.group.id)
    db.add(db_gift)
    db.commit()
    db.refresh(db_gift)
    return db_gift

def update_gift(db: Session, gift_id: int, gift: schemas.GiftCreate):
    r = db.query(models.Gifts).filter(models.Gifts.id == gift_id).update({ "gift": gift.gift, "quantity": gift.quantity, "description": gift.description,"image":gift.image, "idgroup": gift.group.id })
    if r == None:
        return None
    db.commit()
    new_gift = get_gift(db, gift_id)
    return new_gift

def update_gift_image(db: Session, gift_id: int, image: str):
    r = db.query(models.Gifts).filter(models.Gifts.id == gift_id).update({ "image": image })
    print('the update operation results on: ', r)
    if r == None:
        return None
    db.commit()    
    new_gift = get_gift(db, gift_id)
    print(new_gift)
    return new_gift

def delete_gift(db: Session, gift_id: int):
    db_gift = get_gift(db, gift_id)
    db.delete(db_gift)
    db.commit()
    return -1

def add_draw_participant(db: Session, draw_id: int, participant_id: int):
    db_dp = models.DrawParticipants(iddraw = draw_id, idparticipant = participant_id)
    db.add(db_dp)
    db.commit()
    db.refresh(db_dp)
    return db_dp

def get_draw_participants(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    drawParticipants = db.query(models.DrawParticipants).join(models.Draw, models.Draw.id == models.DrawParticipants.iddraw).join(models.Participant, models.Participant.id == models.DrawParticipants.idparticipant).offset(skip).limit(limit).all()
    return drawParticipants

def delete_draw_participant(db: Session, draw_id: int, participant_id: int):
    drawParticipant = db.query(models.DrawParticipants).filter(models.DrawParticipants.iddraw == draw_id, models.DrawParticipants.idparticipant == participant_id).first()
    db.delete(drawParticipant)
    db.commit()
    return -1

def add_draw_gift(db: Session, draw_id: int, gift_id: int):
    db_dg = models.DrawParticipants(iddraw = draw_id, idgift = gift_id)
    db.add(db_dg)
    db.commit()
    db.refresh(db_dg)
    return db_dg

def get_draw_gifts(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    drawGifts = db.query(models.DrawGifts).join(models.Draw, models.Draw.id == models.DrawGifts.iddraw).join(models.Gifts, models.Gifts.id == models.DrawGifts.idgift).offset(skip).limit(limit).all()
    return drawGifts

def delete_draw_gift(db: Session, draw_id: int, gift_id: int):
    drawGift = db.query(models.DrawGifts).filter(models.DrawGifts.iddraw == draw_id, models.DrawGifts.idgift == gift_id).first()
    db.delete(drawGift)
    db.commit()
    return -1


def add_draw_participant_gift(db: Session, draw_participant_gift: schemas.DrawParticipantGiftCreate):
    db_dg = models.DrawParticipantGift(iddraw = draw_participant_gift.draw.id, idparticipant=draw_participant_gift.participant.id, idgift = draw_participant_gift.gift.id, dateselection=draw_participant_gift.dateselection)
    db.add(db_dg)
    db.commit()
    db.refresh(db_dg)
    return db_dg

def get_draw_participants_gifts(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    drawGifts = db.query(models.DrawParticipantGift).join(
        models.Draw, models.Draw.id == models.DrawParticipantGift.iddraw).join(
            models.Participant, models.Participant.id == models.DrawParticipantGift.idparticipant).join(            
                models.Gifts, models.Gifts.id == models.DrawParticipantGift.idgift).offset(skip).limit(limit).all()
    return drawGifts