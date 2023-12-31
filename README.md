# Ticket Show App

The Ticket Show App is a web application designed to showcase tickets. It consists of a backend and a frontend component. The backend handles data storage, processing, and communication, while the frontend provides a user interface to interact with the app.

Users can book show tickets, interact with show details via APIs, and manage bookings.
Admin dashboard featuring revenue statistics and detailed show insights.
Utilized Redis and Celery for backend management with caching for performance, ensured security through token-based authentication.

Tech stack : Vuejs, Python, Flask, Redis, Celery, Bootstrap.

## Folder Structure

### Backend

- `backend/`
  - `db_directory/`
  - `ticket_show_app/`
    - `static/`
      - `pdf/`
    - `templates/`

### Frontend

- `frontend/`
  - `ticket_show_app/`
    - `public/`
    - `src/`
      - `assets/`
      - `components/`
      - `router/`
      - `store/`
      - `views/`

## Backend Setup

1. **Create and activate a virtual environment:**

   ```bash
   cd backend
   virtualenv env
   source env/bin/activate

   Install backend dependencies and run main.py
   
   pip install -r requirements.txt
   python3 main.py
2. **Start the Redis server in a new terminal window:**

   ```bash
   redis-server
   
3. **Run Celery worker:**

   ```bash
   celery -A main.celery worker -l info

4. **Run Celery beat:**

   ```bash
   celery -A main.celery beat --max-interval 1 -l info

   
5. **Start MailHog for email testing (assuming you have MailHog installed):**

   ```bash
   /home/<root>/go/bin/MailHog
    mailhog -api-bind-addr 127.0.0.1:8025 -ui-bind-addr 127.0.0.1:8025 -smtp-bind-addr 127.0.0.1:1025



## Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend/ticket_show_app

2. **Install frontend dependencies:**

   ```bash
    npm install
   
3. **Run the development server**

   ```bash
     npm run dev
