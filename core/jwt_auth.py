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
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
secrete_key = api_settings.JWT_SECRET_KEY

def create_tokens(username, password):
    try:
        custom_auth_backend = CustomAuthBackend()
        user = custom_auth_backend.authenticate(username=username, password=password)
    
        print(user)
        if user:

            # Create access token
            payload = jwt_payload_handler(user)   
            access_token_exp = datetime.now() + timedelta(minutes=30)
            payload['exp'] = (datetime.timestamp(access_token_exp))
            payload['orig_iat'] = int(datetime.timestamp(datetime.now()))
            payload['token_type'] = 'access'
            access_token = jwt_encode_handler(payload)
            print("\n\n")
            print("access_token_exp")
            print(access_token_exp)
            print("\n\n")
            # Create refresh token
            refresh_token_exp = datetime.now() + timedelta(hours=24)
            payload['exp'] = int(datetime.timestamp(refresh_token_exp))
            payload['token_type'] = 'refresh'
            refresh_token = jwt_encode_handler(payload)
            print("\n\n")
            print("refresh_token_exp")
            print(refresh_token_exp)
            print("\n\n")   
            OutstandingRefreshToken.objects.create(user=user, token=refresh_token, expire_at=refresh_token_exp)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            return None
    except Exception as e:
        return f"error: {e}"
    
def refresh_access_token(refresh_token):
    try:
        outstanding_refresh_token = OutstandingRefreshToken.objects.filter(token=str(refresh_token)).first()
        if outstanding_refresh_token:
            if BlacklistedRefreshToken.objects.filter(token=outstanding_refresh_token).exists() == False:
                payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])

                # Check if the token type is 'refresh'
                if payload.get('token_type') == 'refresh':
                    # Set expiration time for the new access token
                    access_token_exp = datetime.now() + timedelta(minutes=1)
                    payload['exp'] =  (datetime.timestamp(access_token_exp))
                    payload['token_type'] = 'access'
                    access_token = jwt_encode_handler(payload)
                    return {'access_token': access_token}
            return  {'detail': "Blacklisted"}

    except jwt.ExpiredSignatureError:
        # Handle expired refresh token
        return None

def blacklist_refresh_token(refresh_token):
    try:
        outstanding_refresh_token = OutstandingRefreshToken.objects.filter(token=str(refresh_token)).first()
        print(outstanding_refresh_token)
        if outstanding_refresh_token:
            balcklisted_refresh_token=BlacklistedRefreshToken.objects.create(token=outstanding_refresh_token)
            print(balcklisted_refresh_token)
            return True
        return False
    except Exception as e:
        pass

