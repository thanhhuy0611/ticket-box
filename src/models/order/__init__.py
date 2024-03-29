from src import db

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