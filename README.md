# Auth-Login through JWT

This project is a Django-based REST API that provides registration, JWT authentication middleware, and CRUD operation APIs.


## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/nayan441/jwt-auth-api.git

2. Create virtual environment and activate:

   ```bash
   virtualenv venv
   source venv/bin/activate (for Ubuntu)
   or
   .\venv\Script\activate  (for Windows)

3. Install required packages:

   ```bash
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate

4. Run script:

   ```bash
   python3 manage.py runserver 8000

The API will be accessible at http://127.0.0.1:8000/.

## Registration API

Endpoint: /api/register/

Method: POST

Request Payload:

    {"username": "your_username",  "email": "your_email@example.com",  "password": "your_password",
        }

## JWT Authentication Middleware
The project includes a custom JWT authentication middleware. JWTs can be obtained by registering and logging in. Use the token for subsequent API requests.

Login:

Endpoint: /api/token/

Method: POST

Request Payload:

    { "username": "nayan",    "password": "12345"}

Logout:

Endpoint: /api/revoke/

Method: POST

Request Payload:

    { "refresh": "<your-refresh-token>"}


## CRUD Operation APIs
Blog Post API

All request have header which we obtain from login api:

    --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzOTQyNjI2LCJpYXQiOjE3MDM5NDIwMjYsImp0aSI6ImQwMjkzMzdmMzQwYTQ4Y2U4NzcyOTc0YjIwOGQyOTc2IiwidXNlcl9pZCI6MX0.4CfXBEbMc7DBBi2gy-hF5wxzLO78xLmiqwBGv3heWXA'

List all blog posts:

Endpoint: /api/blogs/

Method: GET

Retrieve a specific blog post list:

    []

Create blog post:

Endpoint: /api/posts/

Method: POST

Request Payload:

    {
        "title": "n",
        "description": "def put(self,"
    }

Update a blog post:

Endpoint: /api/blogs/<blog_id>/

Method: PUT or PATCH

Request Payload:

    {
    "title": "Updated Post Title",
    "description": "Updated Post Content"
    }

Delete a blog post:

Endpoint:/api/blogs/<blog_id>/

Method: DELETE

## Authentication
To access protected endpoints, include the JWT token in the Authorization header:

    Authorization: Bearer <your_token_here>

