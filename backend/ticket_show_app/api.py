from datetime import datetime, time, date
from flask_jwt_extended import jwt_required
from .workers import send_mails_csv, send_mails_alert
from flask import jsonify
from datetime import datetime, timedelta
from flask import make_response, request
from flask_restful import Resource
from flask_restful import fields, marshal_with, marshal
from flask_restful import reqparse
from werkzeug.exceptions import HTTPException, Conflict
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import generate_password_hash, check_password_hash
from .app import app
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_caching import Cache

from .model import User, Theatre, Show, TicketBooking
from .database import db
import json

from sqlalchemy import func

jwt = JWTManager(app)

cache = Cache(app)


#####################################################
# @app.route('/')
# @cache.cached(timeout=50)
# def home():
#     return "helloworld"


class NotFoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)

#####################################################


user_fields = {
    'id':   fields.Integer,
    'name':    fields.String,
    'email':    fields.String,
    'role': fields.String
}


get_user_login_parser = reqparse.RequestParser()
get_user_login_parser.add_argument('email', required=True)
get_user_login_parser.add_argument('password', required=True)


create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', required=True)
create_user_parser.add_argument('email', required=True)
create_user_parser.add_argument('password', required=True)
# create_user_parser.add_argument('role', required=True, location='args')


##########################################################

class UserRegistrationAPI(Resource):
    @marshal_with(user_fields)
    def post(self):

        args = create_user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)

        # print(username, email, password)

        if username is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1001", error_message="username is required"
            )

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1002", error_message="email is required"
            )

        if "@" not in email:
            raise BusinessValidationError(
                status_code=400, error_code="BE1003", error_message="Invalid email"
            )

        user = User.query.filter_by(email=email).first()

        if user:
            raise BusinessValidationError(
                status_code=400, error_code="BE1004", error_message="Duplicate user"
            )

        user = User(
            name=username,
            email=email,
            password=generate_password_hash(password).decode("utf8"),
            role="user"
        )
        # print("user ", user)
        db.session.add(user)
        db.session.commit()

        return user


class UserLoginAPI(Resource):

    def post(self):
        args = get_user_login_parser.parse_args()
        email = args.get("email", None)
        password = args.get("password", None)

        user = User.query.filter_by(email=email).first()

        if user and user.role == 'user':
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                # Serialize the user data
                response_data = marshal(user, user_fields)
                # Add the access token to the response
                response_data['access_token'] = access_token
                return response_data, 200

            raise BusinessValidationError(
                status_code=400, error_code="BE1004", error_message="Invalid Credentials"
            )

        raise BusinessValidationError(
            status_code=400, error_code="BE1004", error_message="Invalid User Credentials"
        )


##############################################################

admin_fields = {
    'id':   fields.Integer,
    'name':    fields.String,
    'email':    fields.String,
    'role': fields.String
}


get_admin_parser = reqparse.RequestParser()
get_admin_parser.add_argument('email', required=True)
get_admin_parser.add_argument('password', required=True)

create_admin_parser = reqparse.RequestParser()
create_admin_parser.add_argument('username', required=True)
create_admin_parser.add_argument('email', required=True)
create_admin_parser.add_argument('password', required=True)

##############################################################


class AdminRegistrationAPI(Resource):
    @marshal_with(admin_fields)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)

        # print(username, email, password)
        if username is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1001", error_message="username is required"
            )

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1002", error_message="email is required"
            )

        if "@" not in email:
            raise BusinessValidationError(
                status_code=400, error_code="BE1003", error_message="Invalid email"
            )

        user = User.query.filter_by(email=email).first()

        if user:
            raise BusinessValidationError(
                status_code=400, error_code="BE1004", error_message="Duplicate user"
            )

        admin = User(
            name=username,
            email=email,
            password=generate_password_hash(password).decode("utf8"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        return admin


class AdminLoginAPI(Resource):

    def post(self):
        args = get_admin_parser.parse_args()
        email = args.get("email", None)
        password = args.get("password", None)
        # print(email, password)
        admin = User.query.filter_by(email=email).first()

        if admin and admin.role == 'admin':
            if admin and check_password_hash(admin.password, password):
                access_token = create_access_token(identity=admin.id)
                # Serialize the user data
                response_data = marshal(admin, admin_fields)
                # Add the access token to the response
                response_data['access_token'] = access_token
                return response_data, 200

            raise BusinessValidationError(
                status_code=400, error_code="BE1004", error_message="Invalid Credentials"
            )
        raise BusinessValidationError(
            status_code=400, error_code="BE1004", error_message="Invalid admin Credentials"
        )


##############################################################
theatre_fields = {
    'id':   fields.Integer,
    'name':    fields.String,
    'place':    fields.String,
    'location': fields.String,
    'capacity': fields.Integer
}


get_theatre_parser = reqparse.RequestParser()
get_theatre_parser.add_argument('id', location='args')


create_theatre_parser = reqparse.RequestParser()
create_theatre_parser.add_argument('name', required=True,)
create_theatre_parser.add_argument('place', required=True,)
create_theatre_parser.add_argument('location', required=True,)
create_theatre_parser.add_argument('capacity', required=True,)

update_theatre_parser = reqparse.RequestParser()
update_theatre_parser.add_argument('id', required=True)
update_theatre_parser.add_argument('name')
update_theatre_parser.add_argument('place')
update_theatre_parser.add_argument('location')
update_theatre_parser.add_argument('capacity')

get_delete_theatre_parser = reqparse.RequestParser()
get_delete_theatre_parser.add_argument('id', location='args')

##############################################################


class TheatreAPI(Resource):

    @marshal_with(theatre_fields)
    # @cache.cached(timeout=100, query_string=True)
    @jwt_required()
    def get(self):
        args = get_theatre_parser.parse_args()
        id = args.get("id", None)
        if id:
            theatre = Theatre.query.filter_by(id=int(id)).first()
            return theatre
        else:
            theatres = Theatre.query.all()
            return theatres

    @marshal_with(theatre_fields)
    @jwt_required()
    def post(self):
        # print("hi")
        args = create_theatre_parser.parse_args()
        name = args.get("name", None)
        place = args.get("place", None)
        location = args.get("location", None)
        capacity = args.get("capacity", None)

        # print(name, place)

        current_user_id = get_jwt_identity()

        # print(current_user_id)

        admin = User.query.filter_by(id=current_user_id).first()

        # print(admin.role)

        if admin.role != 'admin':
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Admin Access Required"
            )

        if name is None or location is None or place is None or capacity is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Fill all Fields"
            )

        if int(capacity) <= 0:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="capacity should greater than 0"
            )

        theatre = Theatre(
            name=name,
            place=place,
            location=location,
            capacity=capacity
        )
        db.session.add(theatre)
        db.session.commit()

        return theatre

    @marshal_with(theatre_fields)
    @jwt_required()
    def put(self):
        args = update_theatre_parser.parse_args()
        id = args.get("id", None)
        name = args.get("name", None)
        place = args.get("place", None)
        location = args.get("location", None)
        capacity = args.get("capacity", None)

        current_user_id = get_jwt_identity()

        # print(current_user_id)

        admin = User.query.filter_by(id=current_user_id).first()

        # print(admin.role)

        if admin.role != 'admin':
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Admin Access Required"
            )

        if name is None or location is None or place is None or capacity is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Fill all Fields"
            )

        if int(capacity) <= 0:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="capacity should greater than 0"
            )

        theatre = Theatre.query.filter_by(id=id).first()
        if theatre is None:
            raise NotFoundError(status_code=404)

        if name:
            theatre.name = name
            db.session.commit()

        if place:
            theatre.place = place
            db.session.commit()

        if location:
            theatre.location = location
            db.session.commit()

        if capacity:
            theatre.capacity = capacity
            db.session.commit()

        # cache.delete(request.full_path)

        return theatre

    # @marshal_with(theatre_fields)

    @jwt_required()
    def delete(self):
        args = get_delete_theatre_parser.parse_args()
        id = args.get('id', None)
        theatre = Theatre.query.filter_by(id=id).first()
        if theatre is None:
            raise NotFoundError(status_code=404)
        db.session.delete(theatre)
        # cache.delete(request.full_path)
        db.session.commit()


##############################################################
show_fields = {
    'id':   fields.Integer,
    'name':    fields.String,
    'rating':    fields.Float,
    'tags': fields.String,
    'ticket_price': fields.Float,
    'theatre_id': fields.Integer,
    'show_date': fields.String,
    'start_time': fields.String,
    'end_time': fields.String,
    'capacity': fields.Integer,
    'available_tickets': fields.Integer,

}


get_show_parser = reqparse.RequestParser()
get_show_parser.add_argument("theatre_id", location='args')
get_show_parser.add_argument("show_id", location='args')

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument('name')
create_show_parser.add_argument('rating')
create_show_parser.add_argument('tags')
create_show_parser.add_argument('ticket_price')
create_show_parser.add_argument('theatre_id')
create_show_parser.add_argument('start_time')
create_show_parser.add_argument('end_time')
create_show_parser.add_argument('show_date')


update_show_parser = reqparse.RequestParser()
update_show_parser.add_argument('id')
update_show_parser.add_argument('name')
update_show_parser.add_argument('rating')
update_show_parser.add_argument('tags')
update_show_parser.add_argument('ticket_price')
update_show_parser.add_argument('theatre_id')
update_show_parser.add_argument('start_time')
update_show_parser.add_argument('end_time')
update_show_parser.add_argument('show_date')


delete_show_parser = reqparse.RequestParser()
delete_show_parser.add_argument("show_id", location='args')


##############################################################
def generate_cache_key(theatre_id, show_id):
    # Generate a unique cache key based on the parameters
    if show_id:
        return f"_show_api_show:{show_id}"
    else:
        return f"_show_api_theatre:{theatre_id}"


class ShowAPI(Resource):

    @marshal_with(show_fields)
    @jwt_required()
    def get(self):
        args = get_show_parser.parse_args()
        theatre_id = args.get("theatre_id", None)
        show_id = args.get("show_id", None)

        if theatre_id is None and show_id is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE4009", error_message="valid Theatre id or Show id is required")

        cache_key = generate_cache_key(theatre_id, show_id)

        # Check if the data exists in the cache
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        if show_id:
            # print("show_id ", show_id)
            show = Show.query.filter_by(id=int(show_id)).first()
            if show is None:
                raise NotFoundError(status_code=404)
            else:
                cache.set(cache_key, show, timeout=600)
                return show
        else:
            if theatre_id is None:
                raise BusinessValidationError(
                    status_code=400, error_code="BE4001", error_message="valid Theatre id is required")

            theatre = Theatre.query.filter_by(id=int(theatre_id)).first()

            if theatre is None:
                raise NotFoundError(status_code=404)

            cache.set(cache_key, theatre.shows, timeout=600)

            return theatre.shows

    @marshal_with(show_fields)
    @jwt_required()
    def post(self):
        args = create_show_parser.parse_args()
        name = args.get("name", None)
        rating = args.get("rating", None)
        tags = args.get("tags", None)
        ticket_price = args.get("ticket_price", None)
        theatre_id = args.get("theatre_id", None)
        start_time = args.get("start_time", None)
        end_time = args.get("end_time", None)
        show_date = args.get("show_date", None)
        current_user_id = get_jwt_identity()

        # print(current_user_id)

        admin = User.query.filter_by(id=current_user_id).first()

        # print(admin.role)

        if admin.role != 'admin':
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Admin Access Required"
            )

        if name is None or rating is None or ticket_price is None or tags is None or start_time is None or end_time is None or show_date is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Fill all fields"
            )


        if int(rating) <= 0 or int(rating) > 10:
            print(rating)
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="rating should be in scale of 1 - 10"
            )

        if int(ticket_price) <= 0:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="price should greater than 0"
            )
        
        if int(start_time[0:2]) > int(end_time[0:2]) or ( (int(start_time[0:2]) == int(end_time[0:2])) and int(start_time[3:5]) >= int(end_time[3:5])):
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="start time should be greater than end time"
            )
        
        start_time = datetime.strptime(start_time[:5], '%H:%M').time()
        current_date = date.today()

        if show_date == current_date:
            current_time = datetime.now().time()

            if int(start_time[0:2]) < current_time.hour or (int(start_time[0:2]) == current_time.hour and int(start_time[3:5]) <= current_time.minute):
                raise BusinessValidationError(
                    status_code=400, error_code="BE1007", error_message="start time should be greater than current time"
                )
            
        end_time = datetime.strptime(end_time[:5], '%H:%M').time()
        show_date = datetime.strptime(show_date, '%Y-%m-%d').date()
        # print(start_time, end_time, show_date)

        if theatre_id is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE4001", error_message="valid Theatre id is required")

        theatre = Theatre.query.filter_by(id=int(theatre_id)).first()

        show = Show(
            name=name,
            rating=rating,
            tags=tags,
            ticket_price=ticket_price,
            theatre_id=theatre_id,
            start_time=start_time,
            end_time=end_time,
            show_date=show_date,
            available_tickets=theatre.capacity,
            capacity=theatre.capacity
        )

        db.session.add(show)
        db.session.commit()

        cache_key = generate_cache_key(theatre_id, None)
        cache.delete(cache_key)

        return show

    @marshal_with(show_fields)
    @jwt_required()
    def put(self):
        args = update_show_parser.parse_args()
        id = args.get("id", None)
        name = args.get("name", None)
        rating = args.get("rating", None)
        tags = args.get("tags", None)
        ticket_price = args.get("ticket_price", None)
        theatre_id = args.get("theatre_id", None)
        start_time = args.get("start_time", None)
        end_time = args.get("end_time", None)
        show_date = args.get("show_date", None)

        current_user_id = get_jwt_identity()

        # print(current_user_id)

        admin = User.query.filter_by(id=current_user_id).first()

        # print(admin.role)

        if admin.role != 'admin':
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Admin Access Required"
            )
        if id is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1007", error_message="id Required"
            )

        show = Show.query.filter_by(id=int(id)).first()
        if show is None:
            raise NotFoundError(
                status_code=404, error_code="BE5006", error_message="Invalid show id")

        if name is None or rating is None or ticket_price is None or tags is None or start_time is None or end_time is None or show_date is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Fill all fields"
            )


        if int(rating) <= 0 or int(rating) > 10:
            print(rating)
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="rating should be in scale of 1 - 10"
            )

        if int(ticket_price) <= 0:
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="price should greater than 0"
            )

        if int(start_time[0:2]) > int(end_time[0:2]) or ( (int(start_time[0:2]) == int(end_time[0:2])) and int(start_time[3:5]) >= int(end_time[3:5])):
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="start time should be greater than end time"
            )
        
        current_date = date.today()
        current_date = date.today()
        print(show_date, current_date)

        if str(show_date) == str(current_date):
            print(show_date, current_date)
            current_time = datetime.now().time()

            if int(start_time[0:2]) < current_time.hour or (int(start_time[0:2]) == current_time.hour and int(start_time[3:5]) <= current_time.minute):
                raise BusinessValidationError(
                    status_code=400, error_code="BE1007", error_message="start time should be greater than current time"
                )
        
        if name:
            show.name = name
            db.session.commit()
        if rating:
            show.rating = rating
            db.session.commit()
        if tags:
            show.tags = tags
            db.session.commit()
        if ticket_price:
            show.ticket_price = ticket_price
            db.session.commit()
        if theatre_id:
            show.theatre_id = theatre_id
            db.session.commit()
        if show_date:
            # print(show_date)
            show_date = datetime.strptime(show_date[:10], '%Y-%m-%d').date()
            show.show_date = show_date
            db.session.commit()
        if start_time:
            start_time = start_time[:5]
            start_time = datetime.strptime(start_time, '%H:%M').time()
            show.start_time = start_time
            db.session.commit()
        if end_time:
            end_time = end_time[:5]
            end_time = datetime.strptime(end_time, '%H:%M').time()
            show.end_time = end_time
            db.session.commit()

        cache_key = generate_cache_key(show.theatre_id, id)
        cache.delete(cache_key)

        cache_key = generate_cache_key(show.theatre_id, None)
        cache.delete(cache_key)

        return show

    @jwt_required()
    def delete(self):
        args = delete_show_parser.parse_args()
        show_id = args.get("show_id", None)

        if show_id is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE4001", error_message="valid Show id is required")

        show = Show.query.filter_by(id=show_id).first()
        if show is None:
            raise NotFoundError(status_code=404)

        bookings = show.bookings

        db.session.delete(show)

        cache_key = generate_cache_key(None, show_id)
        cache.delete(cache_key)

        cache_key = generate_cache_key(show.theatre_id, None)
        cache.delete(cache_key)

        current_time = datetime.utcnow().time()

        for booking in bookings:
            user = User.query.filter_by(id=booking.user_id).first()

            show_data = {
                "id": show.id,
                "name": show.name,
                "show_date": show.show_date,
                "start_time": show.start_time,
            }

            # print(show.show_date, datetime.now(),
            #       show.start_time, current_time)

            if show.show_date > datetime.now():
                task = send_mails_alert.apply_async(
                    args=[show_data, booking.user_id])

            if show.show_date.date() == datetime.now().date() and show.start_time > current_time:
                task = send_mails_alert.apply_async(
                    args=[show_data, booking.user_id])

        db.session.commit()


##############################################################

booking_fields = {
    'id':   fields.Integer,
    'user_id':    fields.Integer,
    'show_id': fields.Integer,
    'cost':  fields.Float,
    'booking_date': fields.String,
    'num_tickets': fields.Integer,
    'user_rating': fields.Integer,
}


get_booking_parser = reqparse.RequestParser()
get_booking_parser.add_argument('show_id', location='args')


create_booking_parser = reqparse.RequestParser()
# create_booking_parser.add_argument('id')
# create_booking_parser.add_argument('user_id')
create_booking_parser.add_argument('show_id')
create_booking_parser.add_argument('num_tickets')

delete_booking_parser = reqparse.RequestParser()
delete_booking_parser.add_argument('id', location='args')
# update_booking_parser.add_argument('')

##############################################################


class BookingAPI(Resource):
    @marshal_with(booking_fields)
    @jwt_required()
    def get(self):
        args = get_booking_parser.parse_args()
        show_id = args.get('show_id', None)
        if show_id:
            show = Show.query.get(show_id)
            if not show:
                raise NotFoundError(404, 'Show not found')
            bookings = show.bookings
        else:
            # Retrieve all bookings for the user
            current_user = get_jwt_identity()
            user = User.query.get(current_user)
            if not user:
                raise NotFoundError(404, 'User not found')
            bookings = user.get_bookings()

        return bookings

    @marshal_with(booking_fields)
    @jwt_required()
    def post(self):
        args = create_booking_parser.parse_args()
        # user_id = args.get('user_id',None)
        show_id = args.get('show_id', None)
        num_tickets = args.get('num_tickets', None)
        num_tickets = int(num_tickets)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        # print(user)
        if not user:
            raise NotFoundError(404, 'User not found')

        show = Show.query.get(show_id)
        # print(show)
        if not show:
            raise NotFoundError(404, 'Show not found')

        if num_tickets > show.available_tickets:
            raise BusinessValidationError(400, 'Not enough available tickets',
                                          'The show does not have enough available tickets')

        total_cost = num_tickets * show.ticket_price

        booking = TicketBooking(user_id=user_id,
                                show_id=show_id,
                                booking_date=datetime.now(),
                                cost=total_cost,
                                num_tickets=num_tickets)
        db.session.add(booking)
        db.session.commit()
        # print(booking)

        show.available_tickets -= num_tickets
        print(show.available_tickets)
        db.session.commit()

        cache.delete(RevenueAPI.CACHE_KEY)

        cache_key = generate_cache_key(
            theatre_id=show.theatre_id, show_id=show_id)
        cache.delete(cache_key)

        cache_key = generate_cache_key(
            theatre_id=show.theatre_id, show_id=None)
        cache.delete(cache_key)

        return booking

    @jwt_required()
    def delete(self):
        args = delete_booking_parser.parse_args()
        booking_id = args.get('id', None)
        booking = TicketBooking.query.get(booking_id)
        if not booking:
            raise NotFoundError(404, 'Booking not found')

        current_user_id = get_jwt_identity()

        # print(current_user_id)

        # current_user = User.query.filter_by(id=current_user_id).first()

        if booking.user_id != current_user_id:
            raise BusinessValidationError(
                status_code=400, error_code="BE4007", error_message="Invalid booking id")

        show_start_time = datetime.combine(
            booking.show.show_date, booking.show.start_time)
        current_time = datetime.now()
        cancellation_limit = show_start_time - timedelta(hours=1)

        if current_time >= cancellation_limit:
            raise BusinessValidationError(status_code=400, error_code="BE40081",
                                          error_message='Cancellation is only allowed up to 1 hour before the show starts')

        refund_amount = booking.cost

        db.session.delete(booking)
        db.session.commit()

        return {"refund_amount": refund_amount}


############################################################

rating_fields = {
    'id':   fields.Integer,
    'user_id':    fields.Integer,
    'show_id': fields.Integer,
    'cost':  fields.Float,
    'booking_date': fields.String,
    'num_tickets': fields.Integer,
    'user_rating': fields.Integer,
}


create_rating_parser = reqparse.RequestParser()
# create_booking_parser.add_argument('id')
# create_booking_parser.add_argument('user_id')
create_rating_parser.add_argument('show_id')
create_rating_parser.add_argument('booking_id')
create_rating_parser.add_argument('user_rating')


class UserRatingAPI(Resource):
    @marshal_with(rating_fields)
    @jwt_required()
    def post(self):
        args = create_rating_parser.parse_args()
        # user_id = args.get('user_id',None)
        show_id = args.get('show_id', None)
        booking_id = args.get('booking_id', None)
        user_rating = args.get('user_rating', None)

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError(404, 'User not found')
        # print(show_id, booking_id, user_rating)
        if booking_id:
            booking = TicketBooking.query.get(booking_id)
        else:
            raise NotFoundError(404, 'Booking id not found')

        # print(booking)

        if not booking:
            raise NotFoundError(404, 'Booking not found')

        booking.user_rating = user_rating
        db.session.commit()
        return booking

###########################


class RevenueAPI(Resource):

    CACHE_KEY = "_revenue_data"

    @jwt_required()
    def get(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role != 'admin':
            return jsonify({
                'message': 'Valid Admin Credentials required'
            }), 400

        cached_revenue_data = cache.get(RevenueAPI.CACHE_KEY)
        if cached_revenue_data:
            return jsonify(cached_revenue_data)

        # Revenue by Theatre
        revenue_by_theatre = db.session.query(Theatre.name, func.sum(TicketBooking.cost)). \
            join(Show, Theatre.id == Show.theatre_id). \
            join(TicketBooking, Show.id == TicketBooking.show_id).group_by(
            Theatre.name).all()
        revenue_by_theatre = [{"name": row[0], "revenue": float(row[1])}
                              for row in revenue_by_theatre]

        # Revenue by Show
        revenue_by_show = db.session.query(Show.name, func.sum(TicketBooking.cost)). \
            join(TicketBooking, Show.id ==
                 TicketBooking.show_id).group_by(Show.name).all()
        revenue_by_show = [{"name": row[0], "revenue": float(row[1])}
                           for row in revenue_by_show]

        # Revenue Trend Over Time
        revenue_over_time = db.session.query(func.strftime('%Y-%m-%d', TicketBooking.booking_date),
                                             func.sum(TicketBooking.cost)). \
            group_by(func.strftime('%Y-%m-%d', TicketBooking.booking_date)).all()
        revenue_over_time = [{"date": row[0], "revenue": float(row[1])}
                             for row in revenue_over_time]

        # Revenue by Location
        revenue_by_location = db.session.query(Theatre.location, func.sum(TicketBooking.cost)). \
            join(Show, Theatre.id == Show.theatre_id). \
            join(TicketBooking, Show.id == TicketBooking.show_id).group_by(
            Theatre.location).all()
        revenue_by_location = [
            {"location": row[0], "revenue": float(row[1])} for row in revenue_by_location]

        # Revenue Share by Theatre
        total_revenue = db.session.query(func.sum(TicketBooking.cost)).scalar()
        revenue_share_by_theatre = db.session.query(Theatre.name, (func.sum(TicketBooking.cost) / total_revenue) * 100). \
            join(Show, Theatre.id == Show.theatre_id). \
            join(TicketBooking, Show.id == TicketBooking.show_id).group_by(
            Theatre.name).all()
        revenue_share_by_theatre = [
            {"name": row[0], "revenue_share": float(row[1])} for row in revenue_share_by_theatre]

        revenue_data = {
            "revenue_by_theatre": revenue_by_theatre,
            "revenue_by_show": revenue_by_show,
            "revenue_over_time": revenue_over_time,
            "revenue_by_location": revenue_by_location,
            "revenue_share_by_theatre": revenue_share_by_theatre
        }

        cache.set(RevenueAPI.CACHE_KEY, revenue_data, timeout=3600)

        return jsonify(revenue_data)


##################################################################################

email_parser_parser = reqparse.RequestParser()
email_parser_parser.add_argument('theatre_id')


class EmailAPI(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        args = email_parser_parser.parse_args()
        theatre_id = args.get('theatre_id', None)

        # print(theatre_id, user)

        # Triggering the Celery task to send the email to user
        task = send_mails_csv.apply_async(args=[theatre_id, user.email])

        return jsonify({'task_id': task.id, 'message': 'Sending email...'})

##################################################################################


email_status_parser_parser = reqparse.RequestParser()
email_status_parser_parser.add_argument('task_id', location="args")


class EmailStatusAPI(Resource):
    @jwt_required()
    def get(self):
        args = email_status_parser_parser.parse_args()
        task_id = args.get('task_id', None)
        # Check the status of the Celery task
        # print(task_id)
        task = send_mails_csv.AsyncResult(task_id)
        if task.state == 'SUCCESS':
            response = {'status': 'success',
                        'message': 'CSV sent to email successfully!'}
        elif task.state == 'PENDING':
            response = {'status': 'pending',
                        'message': 'Email task is still pending...'}
        else:
            response = {'status': 'failed',
                        'message': 'Failed to send CSV to email.'}

        return response
