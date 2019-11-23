from src import db
class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(1000),nullable= False)
    contain =  db.Column(db.String,nullable= False)
    location = db.Column(db.String,nullable= False)
    banner_url = db.Column(db.String,nullable= True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,nullable = False)
    rating_id = db.Column(db.Integer, nullable = True)
    ticket_id = db.Column(db.Integer, nullable = False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body =  db.Column(db.String,nullable= False)  
    stars = db.Column(db.Integer,nullable = False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # to Users
    user_id = db.Column(db.Integer,nullable = False)
    # to Event
    event_id = db.Column(db.Integer,nullable = False)

db.create_all()