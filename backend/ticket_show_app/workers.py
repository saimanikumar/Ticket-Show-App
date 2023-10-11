import csv
import uuid
from weasyprint import HTML
import os
from .database import db
from .model import User
from jinja2 import Template
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from celery.schedules import crontab
from random import randint
import time
from datetime import datetime
from celery import Celery

from flask import current_app as app

from .model import User, Theatre, Show, TicketBooking
from json import dumps
from httplib2 import Http


celer = Celery("Applications Jobs")


class ContextTask(celer.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


@celer.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    

    sender.add_periodic_task(
        # crontab(hour=23, minute=34),

        # Executes every 1st of every month day_of_month=1
        crontab(hour=10, minute=0, day_of_month=1),
        send_mails_pdf.s(),
    )

    sender.add_periodic_task(
        # crontab(hour=23, minute=34),

        # Executes every day at 6pm
        crontab(hour=18, minute=0),
        send_webhook.s()
    )


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = "1025"
SENDER_ADDRESS = "email@ticketshow-app.com"
SENDER_PASSWORD = ""


def sending_email_pdf(to_address, subject, message, f_path_name):

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    with open(f_path_name, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")

    attach.add_header('Content-Disposition', 'attachment',
                      filename=str("Report.pdf"))
    msg.attach(attach)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()


def format_report_pdf(template_file, user, bookings):
    with open(template_file) as file:
        template = Template(file.read())
        current_month = datetime.now().strftime("%B %Y")
        return template.render(user_name=user.name, current_month=current_month, bookings=bookings)


def create_pdf_report(user, bookings):

    location = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))

    path_name = os.path.join(location, "templates/monthly_report.html")

    message = format_report_pdf(path_name, user, bookings)

    html = HTML(string=message)
    file_name = user.name + " report.pdf"
    path_name = os.path.join(location, f"static/pdf/{file_name}")
    html.write_pdf(target=path_name)
    print(file_name)

    path_name = os.path.join(location, f"static/pdf/{file_name}")
    html.write_pdf(target=path_name)

    return path_name, message


@celer.task()
def send_mails_pdf():
    users = db.session.execute(db.select(User).order_by(User.name)).scalars()
    for user in users:

        user_bookings = user.get_bookings()

        f_path_name, message = create_pdf_report(user, user_bookings)

        sending_email_pdf(user.email, subject="Welcome!",
                          message=message, f_path_name=f_path_name)

#############################################################

@celer.task()
def send_webhook():
    """Hangouts Chat incoming webhook quickstart."""
    url = 'https://chat.googleapis.com/v1/spaces/AAAAYL0mflM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=QZ1lFtZ4iLmo7ZM26QJhDBdghMIQmxhMY7RKwEoHAxw%3D'
    bot_message = {
        'text':
        """
        Hey there! 😊

        It's time to explore some amazing shows and events on Ticket Show App! 🎉

        Don't miss out on the fun and entertainment. Book your tickets now and enjoy the best experiences in town!

        Visit Ticket Show App today to find your perfect show and make wonderful memories with friends and family.

        Happy Ticket Booking! 🎟️🎭
        """
    }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)
################################333

def format_report_csv(theatre_data, shows_data):
    fieldnames = ['Show Name', 'Show Date', 'Show Time']
    rows = []
    for show_data in shows_data:
        row = [show_data['show_name'],
               show_data['show_date'], show_data['show_time']]
        rows.append(row)

    csv_content = ''
    if theatre_data:
        csv_content += f"theatre Name,theatre Location\n{theatre_data['theatre_name']},{theatre_data['theatre_location']}\n\n"

    if rows:
        csv_content += ','.join(fieldnames) + '\n'
        for row in rows:
            csv_content += ','.join(row) + '\n'

    return csv_content


def sending_email_csv(to_address, subject, message, csv_content):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    attachment = MIMEApplication(csv_content, _subtype="csv")
    attachment.add_header('Content-Disposition',
                          'attachment', filename="theatre_info.csv")
    msg.attach(attachment)

    try:
        s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        print("Email send successfully")

    except Exception as e:
        print("Error sending email:", str(e))


@celer.task()
def send_mails_csv(theatre_id, recipient_email):
    theatre = Theatre.query.get(theatre_id)

    theatre_data = {
        'theatre_name': theatre.name,
        'theatre_location': theatre.location
    }

    shows = theatre.shows

    shows_data = []
    for show in shows:
        show_data = {
            'show_name': show.name,
            'show_date': show.show_date.strftime('%Y-%m-%d'),
            'show_time': f"{show.start_time} - {show.end_time}"
        }
        shows_data.append(show_data)

    csv_content = format_report_csv(theatre_data, shows_data)
    sending_email_csv(recipient_email, subject="Show Bookings Report",
                      message="<b>Please find the attached CSV report.</b>", csv_content=csv_content)


#################################################################################

def format_report_alert(user, show, template_file):
    with open(template_file) as file:
        template = Template(file.read())
        print(template)
        return template.render(user_name=user.name, show=show)


def sending_email_alert(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()


def create_html_report(user, show):
    
    location = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))

    path_name = os.path.join(location, "templates/alert_cancel.html")

    message = format_report_alert(user, show, path_name)
    return message



@celer.task()
def send_mails_alert(show, user_id):
    user = User.query.filter_by(id=user_id).first()
    message = create_html_report(user, show)
    sending_email_alert(user.email, subject=f"Event Update - show Cancellation",
                        message=message)




# from twilio.rest import Client

# 
# TWILIO_ACCOUNT_SID = ""
# TWILIO_AUTH_TOKEN = ""
# TWILIO_PHONE_NUMBER = ""



# def send_sms(to_phone_number, body):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#     message = client.messages.create(
#         body=body,
#         from_=TWILIO_PHONE_NUMBER,
#         to=to_phone_number
#     )

#     print("SMS Sent:", message.sid)

# # ...

# @celer.task()
# def send_reminders():
#     
#     users = db.session.query(User).all()

#     for user in users:
#         has_bookings = TicketBooking.query.filter_by(user_id=user.id).first()
#         if not has_bookings:
#             
#             send_sms(user.phone_number, "Please visit/book something on Ticket Show App!")
