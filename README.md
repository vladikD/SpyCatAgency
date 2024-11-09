Requirements

Before you begin, ensure you have the following installed:

Python 3.12

Django 5.1+

Django REST Framework 3.15+

Setup

1. Clone the repository

Clone the repository to your local machine:

git clone https://github.com/vladikD/SpyCatAgency.git

cd SpyCatAgency

2. Set up a virtual environment

python3 -m venv venv

source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install dependencies

Install the required Python packages from requirements.txt:

pip install -r requirements.txt

4.Run migrations to set up the database schema

python manage.py makemigrations

python manage.py migrate

5. Create a superuser (optional, for admin access)

If you want to access the Django admin interface:

python manage.py createsuperuser

6. Start the development server

You can start the application with the following command:

python manage.py runserver

SpyCats Endpoints:

GET /spycats/ — Get a list of all cats

POST /spycats/ — Create a new cat

GET /spycats/{id}/ — Get data about one cat

PUT /spycats/{id}/ — Update information about the cat

DELETE /spycats/{id}/ — Remove a cat

GET /missions/ — Get a list of all missions

POST /missions/ — Create a new mission with goals

GET /missions/{id}/ — Get mission details

PUT /missions/{id}/ — Update the mission

DELETE /missions/{id}/ — Delete mission

POST /missions/{id}/assign_cat/ — Assign a cat to a mission



