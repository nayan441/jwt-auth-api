# middleware.py


from .jwt_auth import refresh_access_token, blacklist_refresh_token
import json
import jwt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from .models import CustomUser

from taskauthlogin.settings import SECRET_KEY
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [r"/api/register/", r"/api/token/", r"/api/revoke/"] :
            response = self.get_response(request)
            return response
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization'].split()

            if len(auth_header) == 2:
                # Extract the token from the Authorization header
                token_key = auth_header[1]
                print(token_key)
                # try:
                payload = jwt.decode(token_key, SECRET_KEY, algorithms=['HS256'])
                print(dir(payload))
                print(payload)
                # Check token expiration
                userid = payload['user_id']
                expire = payload['exp']
                
                if (expire > datetime.now())==False:
                    return JsonResponse({'error': 'Token has expired'}, status=401)

                # Attach the user to the request
                user = CustomUser.objects.filter(id=userid)
                request.user = user
                response = self.get_response(request)
                return response
                # except Exception as e:
                #     return JsonResponse({'error': str(e)}, status=401)
            else:
                return JsonResponse({'error': 'Provide Valid Cred'}, status=401)
        else:
            return JsonResponse({'error': 'Auth token not provided'}, status=401)
       
