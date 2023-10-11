from ticket_show_app import create_app
from flask_cors import CORS

app, api, celery  = create_app()

CORS(app)

from ticket_show_app.api import UserRegistrationAPI,UserLoginAPI, AdminRegistrationAPI, AdminLoginAPI, TheatreAPI, ShowAPI, BookingAPI, RevenueAPI, UserRatingAPI

from ticket_show_app.api import EmailAPI

from ticket_show_app.api import EmailStatusAPI

api.add_resource(UserRegistrationAPI, "/api/user")
api.add_resource(UserLoginAPI, "/api/login")

api.add_resource(AdminRegistrationAPI, "/api/admin")
api.add_resource(AdminLoginAPI, "/api/admin_login")

api.add_resource(TheatreAPI, "/api/theatre")
api.add_resource(ShowAPI, "/api/show")
api.add_resource(BookingAPI, "/api/booking")

api.add_resource(UserRatingAPI, "/api/user/rating")

api.add_resource(RevenueAPI, "/api/revenue")

api.add_resource(EmailAPI, '/api/send_csv_to_email')
api.add_resource(EmailStatusAPI, '/api/email_status')



if __name__ == '__main__':
    app.run(debug=True, port=8080) 


