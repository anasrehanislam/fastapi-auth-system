# app/utils/oauth.py

from app.core.config import settings
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    client_kwargs={'scope': 'email profile'},
)


facebook = oauth.register(
    name='facebook',
    client_id=settings.FACEBOOK_CLIENT_ID,
    client_secret=settings.FACEBOOK_CLIENT_SECRET,
    authorize_url="https://www.facebook.com/v10.0/dialog/oauth",
    access_token_url="https://graph.facebook.com/v10.0/oauth/access_token",
    redirect_uri=settings.FACEBOOK_REDIRECT_URI,
    client_kwargs={"scope": "email"}
)