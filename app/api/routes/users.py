# app/api/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import  UserCreateRequest, UserResponse, RefreshTokenRequest
from app.utils.oauth import google

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.core.security import create_access_token, verify_access_token, hash_password, verify_password
from app.core.config import settings

from fastapi_limiter.depends import RateLimiter

router = APIRouter()

@router.post("/register/email-password", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):

    new_user = register_user(
        email=user.email, 
        password=user.password,
        oauth_provider="email-password", 
        db=db
    )
    return new_user


@router.post("/login/email-password", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Fetch the user from the database
    user = db.query(User).filter(User.email == form_data.username).first()

    # Check if the user exists and if the password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return generate_token_response(user)   

# Refresh token endpoint
@router.post("/token/refresh")
def refresh_access_token(refresh_token_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        # Verify and decode the refresh token using verify_access_token
        payload = verify_access_token(refresh_token_request.refresh_token)

        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Fetch user from the database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return generate_token_response(user)   

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.get("/login/google")
async def login_with_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI  
    return await google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await google.authorize_access_token(request)
    user_info = await google.parse_id_token(request, token)

    # Use the register_user function to register or retrieve the user
    user = register_user(
        email=user_info["email"], 
        oauth_provider="google", 
        oauth_token=token["access_token"], 
        db=db
    )

    # Generate the token response using the generic function
    return generate_token_response(user)


@router.get("/login/facebook")
async def login_with_facebook(request: Request):
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    return await facebook.authorize_redirect(request, redirect_uri)

@router.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    token = await facebook.authorize_access_token(request)
    user_info = await facebook.parse_id_token(request, token)

    # Use the register_user function for Facebook registration
    user = register_user(
        email=user_info["email"], 
        oauth_provider="facebook", 
        oauth_token=token["access_token"], 
        db=db
    )

    # Generate the token response using the generic function
    return generate_token_response(user)   

# Secure route: Get users list
@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Get user by ID
@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Secure route: Delete a user by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(verify_access_token)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


# Generic function to register user from different sources
def register_user(email: str, db: Session, oauth_provider: str = None, oauth_token: str = None, password: str = None):
    # Check if the user already exists
    user = db.query(User).filter(User.email == email).first()

    if user:
        return user  # If user already exists, return the user

    # If no user exists, create a new one
    hashed_password = hash_password(password) if password else None
    user = User(
        email=email,
        hashed_password=hashed_password,
        oauth_provider=oauth_provider,
        oauth_token=oauth_token,
        is_active=True,
        is_superuser=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def generate_token_response(user: User):

     # Create the access token (short-lived)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Create the refresh token (long-lived)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_access_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_info": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser
        }
    }
