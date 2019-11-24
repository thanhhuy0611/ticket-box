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
    
    def tickets(self):
        tickets = Ticket.query.filter_by(event_id = self.id).all()
        return tickets

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)

    def tickets(self):
        order_items = OrderItem.query.filter_by(order_id=self.id)
        tickets = []
        for order_item in order_items:
            ticket = Ticket.query.get(order_item.ticket_id)
            tickets.append(ticket)
        return tickets

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    title = db.Column(db.String)
    event_id = db.Column(db.Integer)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    ticket_id = db.Column(db.Integer)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body =  db.Column(db.String,nullable= False)  
    stars = db.Column(db.Integer,nullable = False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,nullable = False)
    event_id = db.Column(db.Integer,nullable = False)

db.create_all()
