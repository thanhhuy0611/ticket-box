from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from src import *
from src.models.ticket import Ticket
from src.models.order import Order

ticket_blueprint = Blueprint('ticket', __name__, template_folder='../../templates')

@ticket_blueprint.route('/create',methods = ['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        ticket = Ticket(title=request.form['title'], quantity=request.form['quantity'], event_id = request.form['event_id'])
        db.session.add(ticket)
        db.session.commit()
        return "OK"
    pass


@ticket_blueprint.route('/purchase',methods = ['GET','POST'])
@login_required
def purchase():
    if request.method == 'POST':
        order = Order(event_id = request.form['event_id'], user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        event = Event.query.get(request.form['event_id'])
        for ticket in event.tickets():
            selected_ticket = request.form['ticket_id_{0}'.format(ticket.id)]
            selected_ticket_quantity = request.form['ticket_count_{0}'.format(ticket.id)]
            if selected_ticket and int(selected_ticket_quantity) > 0:
                numberrrr = int(request.form['ticket_count_{0}'.format(ticket.id)])
                for number in range(0, numberrrr):
                    order_item = OrderItem(order_id=order.id, ticket_id=ticket.id)
                    ticket.quantity -= 1
                    db.session.add(order_item)
                    db.session.commit()
                ticket.quantity -= numberrrr
    return redirect(url_for('user.orders'))