# jwt_auth.py

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from .custom_auth import CustomAuthBackend
from rest_framework_jwt.settings import api_settings
from .models import OutstandingRefreshToken, BlacklistedRefreshToken

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def create_tokens(username, password):
    custom_auth_backend = CustomAuthBackend()
    user = custom_auth_backend.authenticate(username=username, password=password)
    print(user)
    if user:

        payload = jwt_payload_handler(user)

        access_token_exp = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
        refresh_token_exp = datetime.utcnow() + api_settings.JWT_REFRESH_EXPIRATION_DELTA
        payload['exp'] = str(access_token_exp)
        payload['orig_iat'] = str(datetime.utcnow())

        access_token = jwt_encode_handler(payload)

        # Create refresh token
        payload['exp'] = refresh_token_exp
        payload['token_type'] = 'refresh'
        refresh_token = jwt_encode_handler(payload)
       
        OutstandingRefreshToken.objects.create(user=user, token=refresh_token, expire_at=access_token_exp)


        return {'access_token': access_token, 'refresh_token': refresh_token}
    else:
        return None

def refresh_access_token(refresh_token):
    try:
        print("refresh_access_token")
        print("refresh_access_token")
        outstanding_refresh_token = OutstandingRefreshToken.objects.filter(token=str(refresh_token)).first()
        print("outstanding_refresh_token")
        print(outstanding_refresh_token)

        if outstanding_refresh_token:
            if BlacklistedRefreshToken.objects.filter(token=outstanding_refresh_token).exists() == False:
                payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

                # Check if the token type is 'refresh'
                if payload.get('token_type') == 'refresh':
                    # Set expiration time for the new access token
                    payload['exp'] = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
                    return {'access_token': jwt_encode_handler(payload)}
            return  {'detail': "Blacklisted"}

    except jwt.ExpiredSignatureError:
        # Handle expired refresh token
        return None

def blacklist_refresh_token(refresh_token):
    print("blacklist_refresh_token")
    print("refresh_token")
    print(refresh_token)
    outstanding_refresh_token = OutstandingRefreshToken.objects.filter(token=str(refresh_token)).first()
    print(outstanding_refresh_token)
    if outstanding_refresh_token:
        balcklisted_refresh_token=BlacklistedRefreshToken.objects.create(token=outstanding_refresh_token)
        print(balcklisted_refresh_token)
        return True
    return False