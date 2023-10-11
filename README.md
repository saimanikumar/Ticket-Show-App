## Ticket Show App

## The Ticket Show App is a web application designed to showcase tickets. It consists of a backend and a frontend component. The backend handles data storage, processing, and communication, while the frontend provides a user interface to interact with the app.

Folder Structure:

backend/
│   db_directory/
│   ticket_show_app/
│   └─── static/
│   │   └─── pdf/
│   ├─── templates/

frontend/
└─── ticket_show_app/
│       public/
│       └─── src/
│       │   ├─── assets/
│       │   ├─── components/
│       │   ├─── router/
│       │   ├─── store/
│       │   └─── views/

## Backend Setup:

# 1. Create and activate a virtual environment:
   cd backend
   virtualenv env
   source env/bin/activate

# 2. Install backend dependencies and main.py file:
   pip install -r requirements.txt
   python3 main.py

# 3. Start the Redis server in a new terminal window:
   redis-server

# 4. Run Celery worker:
   celery -A main.celery worker -l info

# 5. Run Celery beat:
   celery -A main.celery beat --max-interval 1 -l info

# 6. Start MailHog for email testing (assuming you have MailHog installed):
   /home/y20cs045/go/bin/MailHog
   mailhog -api-bind-addr 127.0.0.1:8025 -ui-bind-addr 127.0.0.1:8025 -smtp-bind-addr 127.0.0.1:1025

## Frontend Setup:

# 1. Navigate to the frontend directory:
   cd frontend/ticket_show_app

# 2. Run the frontend development server:
   npm install
   npm run dev

# Usage:

- Open your browser and visit localhost to access the Ticket Show App frontend.

