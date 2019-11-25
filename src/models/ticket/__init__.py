from src import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    title = db.Column(db.String)
    event_id = db.Column(db.Integer)