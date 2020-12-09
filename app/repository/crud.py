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


def get_participant_byemail(db: Session, participant: str):
    return db.query(models.Participant).join(models.Group, models.Group.id == models.Participant.idgroup).filter(models.Participant.email == participant).first()

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

def add_draw_participants(db: Session, draw_id: int, participants: schemas.ParticipantList):
    print('add_draw_participants:', draw_id, participants)
    r = db.query(models.DrawParticipants).filter(models.DrawParticipants.iddraw == draw_id).delete(synchronize_session=False)
    print("delete drawparticipants result:", r)
    count = 0
    for participant in participants.participants:
        print('participant:',participant)
        db_dp = models.DrawParticipants(iddraw = draw_id, idparticipant = participant.id)    
        db.add(db_dp)
        count = count + 1
    db.commit()    
    return count

# SELECT kmgm00t.id iddraw, kmgm00t.title title, kmgm00t.fordate fordate, kmgm00t.status status, 
#         kmgm11t.id idparticipant, kmgm11t.participant participant, kmgm11t.email email, 
#         kmgm10t.id idgroup, kmgm10t.groupname groupname, kmgm10t.description description
#   FROM kmgm01t INNER JOIN kmgm00t ON kmgm01t.iddraw = kmgm00t.id
#     INNER JOIN kmgm11t ON kmgm01t.idparticipant = kmgm11t.id 
#     INNER JOIN kmgm10t ON kmgm11t.idgroup = kmgm10t.id

def get_draw_participants(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    print('get_draw_participants({})'.format(draw_id))
    drawParticipants = db.query(models.DrawParticipants, models.Draw, models.Participant, models.Group)\
        .filter(models.DrawParticipants.iddraw==draw_id)\
            .join(models.Draw, models.Draw.id == models.DrawParticipants.iddraw)\
            .join(models.Participant, models.Participant.id == models.DrawParticipants.idparticipant)\
            .join(models.Group, models.Group.id == models.Participant.idgroup)\
                .offset(skip).limit(limit).all()    
    drawReady = False
    draw = None
    participants = []
    for row in drawParticipants:        
        oDraw = row[1]
        oParticipant = row[2]        
        oGroup = row[3]
        if not drawReady:
            draw = { 'id': oDraw.id, 'title': oDraw.title, 'status':oDraw.status, 'fordate':oDraw.fordate }
            drawReady = True
        participant = { 'id': oParticipant.id, 'participant': oParticipant.participant, 'email': oParticipant.email, 'group': { 'id': oGroup.id, 'groupname': oGroup.groupname, 'description': oGroup.description } }
        participants.append(participant)
    result = {'draw': draw, 'participants': participants }
    
    return result

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

def add_draw_gifts(db: Session, draw_id: int, gifts: schemas.GiftList):
    print('data in come:',gifts)
    count = 0
    r = db.query(models.DrawGifts).filter(models.DrawGifts.iddraw == draw_id).delete(synchronize_session=False)
    print("delete drawgifts result:", r)
    for gift in gifts.gifts:
        print('gift:',gift)
        db_dg = models.DrawGifts(iddraw = draw_id, idgift = gift.id)
        db.add(db_dg)
        count = count + 1
    db.commit()    
    return count

def get_draw_gifts(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    print('get_draw_gifts({})'.format(draw_id))
    drawGifts = db.query(models.DrawGifts, models.Draw, models.Gifts, models.Group)\
        .filter(models.DrawGifts.iddraw==draw_id)\
            .join(models.Draw, models.Draw.id == models.DrawGifts.iddraw)\
            .join(models.Gifts, models.Gifts.id == models.DrawGifts.idgift)\
            .join(models.Group, models.Group.id == models.Gifts.idgroup)\
                .offset(skip).limit(limit).all()    
    drawReady = False
    draw = None
    gifts = []
    for row in drawGifts:        
        oDraw = row[1]
        oGift = row[2]        
        oGroup = row[3]
        if not drawReady:
            draw = { 'id': oDraw.id, 'title': oDraw.title, 'status':oDraw.status, 'fordate':oDraw.fordate }
            drawReady = True
        gift = { 'id': oGift.id, 'gift': oGift.gift, 'quantity': oGift.quantity, 'image': oGift.image, 'description': oGift.description, 'group': { 'id': oGroup.id, 'groupname': oGroup.groupname, 'description': oGroup.description } }
        gifts.append(gift)
    result = {'draw': draw, 'gifts': gifts }    
    return result

def delete_draw_gift(db: Session, draw_id: int, gift_id: int):
    drawGift = db.query(models.DrawGifts).filter(models.DrawGifts.iddraw == draw_id, models.DrawGifts.idgift == gift_id).first()
    db.delete(drawGift)
    db.commit()
    return -1

def get_draw_participants_gifts(db: Session, draw_id: int, skip: int = 0, limit: int = 100):
    drawGifts = db.query(models.DrawParticipantGift, models.Gifts)\
        .join(models.Draw, models.Draw.id == models.DrawParticipantGift.iddraw)\
            .join(models.Gifts, models.Gifts.id == models.DrawParticipantGift.idgift).all()
    if drawGifts:
        elements = []
        for drawGift in drawGifts:
            oSelected = drawGift[0]
            oGift = drawGift[1]
            element = { 'idparticipant': oSelected.idparticipant, 'idgift': oGift.id, 'alias': oSelected.dsgift, 'evidence': oSelected.dateselection, 'gift': oGift.gift, 'description': oGift.description, 'image': oGift.image }            
            print('the selected gift is: ', element)
            elements.append(element)

        return { 'data': elements }
    else:
        return None


def get_draw_participant_gift(db: Session, draw_id: int, participant_id: int):
    drawGift = db.query(models.DrawParticipantGift, models.Gifts).filter(models.DrawParticipantGift.idparticipant==participant_id)\
        .join(models.Draw, models.Draw.id == models.DrawParticipantGift.iddraw)\
            .join(models.Gifts, models.Gifts.id == models.DrawParticipantGift.idgift).first()
    if drawGift:
        oSelected = drawGift[0]
        oGift = drawGift[1]
        result = {  'idparticipant': participant_id, 'idgift': oGift.id, 'alias': oSelected.dsgift, 'evidence': oSelected.dateselection, 'gift': oGift.gift, 'description': oGift.description, 'image': oGift.image }
        print('the selected gift is: ', result)
        return result
    else:
        return None
    

def set_draw_publish(db: Session, draw_id: int, draw_publish: schemas.DrawPublishCreate):
    publish = models.DrawPublish(iddraw=draw_id, startdate=draw_publish.startDate, access_code=draw_publish.access_code)
    db.add(publish)
    r = db.query(models.Draw).filter(models.Draw.id == draw_id).update({ "status": 'onlive' })
    print('the update status draw on: ', r)
    db.commit()
    db.refresh(publish)
    return publish

def get_draw_publish(db: Session, draw_id: int):
    publish = db.query(models.DrawPublish, models.Draw)\
        .filter(models.DrawPublish.iddraw==draw_id)\
            .join(models.Draw, models.Draw.id == models.DrawPublish.iddraw).first()
    if publish:
        oPublish = publish[0]
        oDraw = publish[1]
        print(oDraw, oPublish)
        draw = { 'id': oDraw.id, 'title': oDraw.title, 'status':oDraw.status, 'fordate':oDraw.fordate }
        result = { 'draw': draw, 'startDate': oPublish.startdate, 'endDate': oPublish.enddate, 'access_code': oPublish.access_code }
        print('result', result)
        return result
    else:
        return None

def set_draw_publish_end(db: Session, draw_id: int, enddate: str):
    r = db.query(models.DrawPublish).filter(models.DrawPublish.iddraw == draw_id).update({ "enddate": enddate })
    print('the update operation draw publish on: ', r)
    r = db.query(models.Draw).filter(models.Draw.id == draw_id).update({ "status": 'closed' })
    print('the update status draw on: ', r)
    if r == None:
        return None
    db.commit()    
    return r

def get_access(db:Session, participant: str, access_code: str):
    # print('Start search with params {}:{}'.format(participant, access_code))
    sql = """SELECT kmgm01t.iddraw AS kmgm01t_iddraw, 
                    kmgm01t.idparticipant AS kmgm01t_idparticipant, 
                    kmgm11t.id AS kmgm11t_id, 
                    kmgm11t.participant AS kmgm11t_participant, 
                    kmgm11t.email AS kmgm11t_email, 
                    kmgm11t.idgroup AS kmgm11t_idgroup, 
                    kmgm00t.id AS kmgm00t_id, 
                    kmgm00t.title AS kmgm00t_title, 
                    kmgm00t.fordate AS kmgm00t_fordate, 
                    kmgm00t.status AS kmgm00t_status, 
                    kmgm99t.iddraw AS kmgm99t_iddraw, 
                    kmgm99t.startdate AS kmgm99t_startdate, 
                    kmgm99t.enddate AS kmgm99t_enddate, 
                    kmgm99t.access_code AS kmgm99t_access_code, 
                    kmgm99t.tmstmp AS kmgm99t_tmstmp
                FROM kmgm01t INNER JOIN kmgm11t 
                  ON kmgm11t.id = kmgm01t.idparticipant INNER JOIN kmgm99t 
                  ON kmgm99t.iddraw = kmgm01t.iddraw INNER JOIN kmgm00t 
                  ON kmgm00t.id = kmgm01t.iddraw
                WHERE kmgm11t.email = '{}' and kmgm99t.access_code='{}'""".format(participant, access_code)
    access = db.execute(sql).first() 
    print('access',access)
    if access:
        #  (1, 1, 1, 'Alberto Farias', 'carlos.farias@gft.com', 2, 1, 'Cierre de año 2020', datetime.date(2020, 12, 17), 'onlive', 1, datetime.date(2020, 12, 8), None, '12345', datetime.datetime(2020, 12, 8, 9, 36, 59))
        draw = { 'id': access[0], 'title': access[7], 'status':access[9], 'fordate':access[8] }
        participant = { 'id': access[2], 'participant': access[3], 'email': access[4], 'group' : {'id': access[5], 'groupname': '', 'description': '' } }
        print('Previous result', draw, participant)
        participants = [participant]
        result = {'draw': draw, 'participants':participants}
        return result
    else:
        return None

def get_available_gifts(db:Session, iddraw: int, idgroup: int):
    sql = """SELECT dg.iddraw AS iddraw, dg.idgift AS idgift, RIGHT(md5(CONCAT(g.id, g.gift)), 7) alias, g.idgroup As idgroup 
        FROM kmgm02t dg INNER JOIN kmgm12t g 
          ON dg.idgift = g.id 
        WHERE dg.idgift NOT IN 
           (SELECT idgift FROM kmgm20t WHERE iddraw = dg.iddraw)
           AND g.idgroup = {} AND dg.iddraw = {} ORDER BY alias;
          """.format(idgroup, iddraw)
    result = db.execute(sql)
    gifts = []
    for row in result:
        gift = { 'iddraw': row[0], 'alias': row[2], 'idgroup': row[3] }
        gifts.append(gift)
    print('results from query:',gifts)
    results = { 'gifts': gifts }
    return results

def get_gift_byalias(db: Session, alias: str):
    sql = "SELECT id FROM kmgm12t WHERE RIGHT(md5(CONCAT(id, gift)), 7) = '{}';".format(alias)
    result = db.execute(sql)
    if result:
        for row in result:
            print("alias found: ", row[0])
        return row[0]
    else:
        return None

def add_draw_participant_gift(db: Session, drawid: int, participantid: int, alias: str):
    # first at all. be sure the participant doesn't pick one yet:
    sql = "SELECT count(idparticipant) FROM kmgm20t WHERE iddraw='{}' and idparticipant = '{}';".format(drawid, participantid)
    result = db.execute(sql)
    count=1
    if result:
        for row in result:
            print("record found: ", row[0])
            count = row[0]
    else:
        return None
    if count>0:
        return count
    giftid = get_gift_byalias(alias=alias, db=db)
    if giftid:
        db_dg = models.DrawParticipantGift(iddraw = drawid, idparticipant=participantid, idgift = giftid, dsgift=alias)
        print('record to add:', db_dg)
        db.add(db_dg)
        db.commit()
        return db_dg
    else:
        return None
