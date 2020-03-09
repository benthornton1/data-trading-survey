from app import app, db
from app.models import User, Study, Card, UserGroup, CardSet

try:
    # Card.query.delete()
    cards = Card.query.all()
    for card in cards:
        db.session.delete(card)
    CardSet.query.delete()
    User.query.delete()
    UserGroup.query.delete()
    Study.query.delete()
    
    # im = images.delete()
    # im.execute()
    # cd = cards.delete().all()
    # cd.execute()
    # db.session.commit()

    uAdmin = User()
    # uParticipant = User()
    # s = Study()
    # # i = Image()
    # c = Card()
    # cs = CardSet()
    # cs2 = CardSet()
    
    uAdmin.email = "a@a.com"
    uAdmin.set_password("hello")
    uAdmin.is_admin = True
    db.session.add(uAdmin)
    db.session.commit()

    # print("Admin Creation Successful")

    # user = User.query.filter_by(email=uAdmin.email).first_or_404()

    # s.name = "IoT Data Trading"
    # s.meausres = "Sensitivity"
    # s.data_values = 1
    # s.number_of_columns = 3
    # s.creator = user.id
    # db.session.add(s)
    # db.session.commit()
    # print("Study Creation Successful")
    
    # study = Study.query.filter_by(name=s.name).first_or_404()


    # i.path = "/path/to/image"
    # i.creator = user.id
    # db.session.add(i)
    # db.session.commit()
    # print("Image Creation Successful")
    
    # image = Image.query.filter_by(path=i.path).first_or_404()
    
    # c.name = "Social Media"
    # c.creator = user.id
    # c.images = [image]
    # db.session.add(c)
    # db.session.commit()
    # print("Card Creation Successful")

    # card = Card.query.filter_by(name=c.name).first_or_404()
    
    # cs.name="Card Set 1"
    # cs.creator = user.id
    # cs.cards = [card]
    
    # cs2.name="Card Set 2"
    # cs2.creator = user.id
    # cs2.cards = [card]
    # db.session.add(cs)
    # db.session.add(cs2)
    # db.session.commit()
    # print("CardSet Creation Successful")
    
    # card_set = CardSet.query.filter_by(name=cs.name).first_or_404()
    # card_set2 = CardSet.query.filter_by(name=cs2.name).first_or_404()
    # study.card_sets.append(card_set)
    # study.card_sets.append(card_set2)

    # # image = Image.query.filter_by(image=i.image).first_or_404()

    # uParticipant.email = "p@p.com"
    # uParticipant.set_password("hello")
    # uParticipant.study = study.id
    # uParticipant.parent_id = user.id
    # db.session.add(uParticipant)
    # db.session.commit()
    # print("Participant Creation Successful")

    

except Exception as error:
    print(str(error))
    db.session.rollback()



