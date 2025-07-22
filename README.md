# Tripease

A three-tier web application for hotel and tourism management.

## Stack
- Backend: Django (Python)
- Database: PostgreSQL
- Frontend: Django Templates (HTML, CSS, Tailwind CSS, JavaScript)

## Major Modules
- Hotel Management (Rooms, Bookings, Orders, Stock)
- Tourism Management (Tour Packages, Bookings)
- Admin & Reports (Dashboard, Reports, User Management)
- Feedback & Ratings
- Notifications
- Support
- Authentication
- Payment
- Cart

## Setup Instructions

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure PostgreSQL credentials in `tripease_backend/settings.py`.
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Tailwind CSS
- Tailwind CSS will be set up for styling Django templates.

---

This project is modular and ready for further development of each feature. 