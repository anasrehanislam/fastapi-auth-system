# FastAPI Authentication & Authorization System

This project implements an authentication and authorization system using **FastAPI** with JWT-based authentication, OAuth integration (Google & Facebook), and role-based access control. The system also includes rate limiting to protect the API from excessive requests.

## Technologies Used

- **Python** 3.10
- **FastAPI** (Web framework)
- **OAuth 2.0** (Google, Facebook login)
- **JWT** (JSON Web Tokens)
- **Redis** (Rate limiting)
- **PostgreSQL** (or SQLite for local development)

---

## Setup Instructions

### 1. Clone the Repository


git clone https://github.com/your-repo/fastapi-auth-system.git
cd fastapi-auth-system


### 2. Set Up a Virtual Environment


python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### 3. Configure Environment Variables

Created a `.env` file in the root directory and populate it with the following environment variables:

SECRET_KEY=9a2e0b1d73f94bf5a73bbcf6d88d1f87e72a0b1d51c08f89b4c82fd964d93d51
API_KEY=b8947b1e7f1a4f78a0d5d12b9b1e8d73a4e9fd1c7e92a3b4c6f28bf972c7e91a

DATABASE_URL=sqlite+aiosqlite:///./test.db


GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/users/google/callback

FACEBOOK_CLIENT_ID=your_google_client_id
FACEBOOK_CLIENT_SECRET=your_google_client_secret
FACEBOOK_REDIRECT_URI=http://localhost:8000/api/v1/users/facebook/callback


# Rate Limiting
REDIS_URL=redis://localhost:6379


Replace placeholders (`your_google_client_id`, etc.) with the actual values.

### 4. Run Database Migrations

alembic revision --autogenerate -m "Recreate users table"
alembic upgrade head


### 5. Start the Server


uvicorn app.main:app --reload


---

## API Endpoints

### 1. **User Registration (Email & Password)**

- **Method**: `POST`
- **Endpoint**: `/users/register/email-password`
- **Description**: Register a new user using an email and password.
- **Payload**:
    json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    

### 2. **Login (Email & Password)**

- **Method**: `POST`
- **Endpoint**: `/users/login/email-password`
- **Description**: Log in using an email and password.
- **Payload** (Form Data):
    json
    {
        "username": "user@example.com",
        "password": "password123"
    }
    

### 3. **Get All Users**

- **Method**: `GET`
- **Endpoint**: `/users`
- **Description**: Retrieve a list of all registered users. (Rate limited: 5 requests per minute)

### 4. **Admin Dashboard (Role-Based Access)**

- **Method**: `GET`
- **Endpoint**: `/admin-dashboard`
- **Description**: Access restricted to users with the "admin" role.

### 5. **Google Login**

- **Method**: `GET`
- **Endpoint**: `/login/google`
- **Description**: Initiate Google OAuth login flow.

### 6. **Google Callback**

- **Method**: `GET`
- **Endpoint**: `/google/callback`
- **Description**: Google OAuth callback URL for handling Google login.

### 7. **Facebook Login**

- **Method**: `GET`
- **Endpoint**: `/login/facebook`
- **Description**: Initiate Facebook OAuth login flow.

### 8. **Facebook Callback**

- **Method**: `GET`
- **Endpoint**: `/facebook/callback`
- **Description**: Facebook OAuth callback URL for handling Facebook login.

### 9. **Token Refresh**

- **Method**: `POST`
- **Endpoint**: `/token/refresh`
- **Description**: Refresh access token using a valid refresh token.
- **Payload**:
    json
    {
        "refresh_token": "your-refresh-token"
    }
    

---

## OAuth Setup (Google & Facebook)

To enable Google and Facebook login, the client needs to create OAuth credentials for both services and provide them in the `.env` file.

### 1. **Google Client Keys**

- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create new **OAuth 2.0 credentials**.
- Set the **redirect URI** to `http://localhost:8000/google/callback`.
- Add the following keys to the `.env` file:
    env
    GOOGLE_CLIENT_ID=your-google-client-id
    GOOGLE_CLIENT_SECRET=your-google-client-secret
    GOOGLE_REDIRECT_URI=http://localhost:8000/google/callback
    

### 2. **Facebook Client Keys**

- Go to [Facebook for Developers](https://developers.facebook.com/).
- Create a new app and get **OAuth credentials**.
- Set the **redirect URI** to `http://localhost:8000/facebook/callback`.
- Add the following keys to the `.env` file:
    env
    FACEBOOK_CLIENT_ID=your-facebook-client-id
    FACEBOOK_CLIENT_SECRET=your-facebook-client-secret
    FACEBOOK_REDIRECT_URI=http://localhost:8000/facebook/callback
    

---

## Rate Limiting

To prevent abuse, rate limiting is implemented using Redis. Make sure Redis is running on your local machine or server. You can adjust the rate limits in the route dependencies, e.g., `RateLimiter(times=10, seconds=60)` means 10 requests per minute.

---

## Testing

To run the tests, use the following command:
pytest


Ensure the Redis server is running to avoid errors related to rate limiting during tests.



