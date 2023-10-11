from datetime import datetime
from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def get_bookings(self):
        return TicketBooking.query.filter_by(user_id=self.id).all()


class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    place = db.Column(db.String(255))
    location = db.Column(db.String(255))
    capacity = db.Column(db.Integer, default=0)
    shows = db.relationship('Show', backref='theatre', cascade="all, delete")


    def __repr__(self):
        return f"<Theatre {self.name}>"


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.Float)
    tags = db.Column(db.String(255))
    ticket_price = db.Column(db.Float)
    show_date = db.Column(db.DateTime)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    capacity = db.Column(db.Integer)
    available_tickets = db.Column(db.Integer) 
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    bookings = db.relationship('TicketBooking', backref='show', cascade="all, delete")

    def __repr__(self):
        return f"<Show {self.name}>"


class TicketBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    cost = db.Column(db.Float)
    num_tickets = db.Column(db.Integer)
    user_rating = db.Column(db.Integer, default=0)

    
    def __repr__(self):
        return f"<TicketBooking {self.id}>"
