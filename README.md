# Starnavi test task

### How to run locally
Did not use anything like docker, docker-compose because they were not mentioned in the technical requirements
- Project was implemented using `python3.9`
- Make sure you have enabled your virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Create the database: `python manage.py makemigrations && migrate`
- Create superuser: `python manage.py initadmin`. Default superuser credentials are listed below
- Run tests: `python manage.py test apps`
- Run local server: `python manage.py runserver`

### Default superuser credentials
Login: `admin@gmail.com`<br/>
Password: `admin`

### Object of this task
```
Object of this task is to create a simple REST API. You can use one framework from this list 
(Django Rest Framework, Flask or FastAPI) and all libraries which you prefer to use with 
this frameworks.
```
My choice fell on:
- `Django Rest Framework`
- `rest_framework.authtoken` for authentication
- `factory_boy` as a helper for tests
- `black` && `isort` for code formatting
- Django's default sqlite3 database

### Basic models
``` 
Basic models:
● User
● Post (always made by a user)
```

- `User` model is implemented in `apps.authorization` app
- `Post` model is implemented in `apps.posts` app
- `Like` model was created on my initiative. It is used to save likes of specific post

### Basic features
```
Basic Features:
● user signup
● user login
● post creation
● post like
● post unlike
● analytics about how many likes was made. Example url 
/api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics 
aggregated by day.
● user activity an endpoint which will show when user was login last time and when he 
mades a last request to the service.
```
- `user signup`, `user login`, `user activity endpoint` were implemented in `authorization` app
- `post creation`, `post like`, `post unlike`, `post analytics` features are implemented in `posts` app

### Requirements
```
Requirements:
● Implement token authentication (JWT is prefered)
```
Implemented token authentication using `rest_framework.authtoken`
