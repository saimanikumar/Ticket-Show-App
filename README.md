# Ticket Show App

The Ticket Show App is a web application designed to showcase tickets. It consists of a backend and a frontend component. The backend handles data storage, processing, and communication, while the frontend provides a user interface to interact with the app.

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

