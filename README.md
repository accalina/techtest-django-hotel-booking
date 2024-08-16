# techtest-django-hotel-booking
Simple django hotel booking backend for technical test

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or later
- pip (Python package installer)
- Docker (for Docker setup)
- Docker Compose (for Docker Compose setup)

## Installation

### With Docker

1. **Clone the Repository**
Same as without Docker, this command clones the repository to your local machine and navigates into the project directory.
```sh
$ git clone https://github.com/accalina/techtest-django-hotel-booking
$ cd techtest-django-hotel-booking
```

2. **Build and Start Containers**
Builds the Docker images defined in your docker-compose.yml file and starts the containers.
```sh
$ docker-compose up --build
```

### Without Docker

1. **Clone the Repository**
```sh
$ git clone https://github.com/accalina/techtest-django-hotel-booking
$ cd techtest-django-hotel-booking
```

2. **Create and Activate a Virtual Environment**
This creates an isolated Python environment to avoid conflicts with other projects and activates it.
```sh
$ python -m venv env
$ source env/bin/activate  # On Windows use `env\Scripts\activate`
$ cd backend
```

3. **Install Dependencies**
Installs all the required Python packages for the project as listed in the requirements.txt file.
```sh
$ pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a .env file in the project root and add necessary environment variables. Example:
```
ENV=dev   # use 'prod' for docker environtment
SECRET_KEY=your_secret_key
WHITELIST_HOSTS=localhost
```

5. **Run Migrations**
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```
Generates and applies database migrations to set up your database schema based on your Django models.

6. **Collect Static Files**
```sh
$ python manage.py collectstatic
```
Gathers all static files (CSS, JavaScript, images) into a single directory for serving in production.

7. **Create a Superuser**
Creates an admin account to access the Django admin interface.
```sh
$ python manage.py createsuperuser
```

8. **Start the Development Server**
Starts the Django development server at http://localhost:8000/ where you can access your application.
```sh
$ python manage.py runserver
```

9. **Run Tests**
Runs the project's test suite to ensure that your application is working as expected.
```sh
$ python manage.py test
```