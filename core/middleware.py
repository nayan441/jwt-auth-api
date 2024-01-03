# middleware.py



import jwt
from .models import CustomUser
from django.conf import settings
from taskauthlogin.settings import SECRET_KEY
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            exempted_urls = ['/admin/', "/api/register/", "/api/token/", "/api/token/refresh/", "/api/all/",]
            if any(request.path.startswith(url) for url in exempted_urls):
                print("middleware skipped for: ", request.path)
                return self.get_response(request)

            if 'Authorization' in request.headers:
                print("==inside middleware=="*5)
                auth_header = request.headers['Authorization'].split()

                if len(auth_header) == 2:
                    # print("\n\n\n")
                    # print(jwt.decode(token_key, settings.SECRET_KEY, algorithms=['HS256']))
                    # print("\n\n\n")

                    # try:
                        token_key = auth_header[1]
                        payload = jwt.decode(token_key, settings.SECRET_KEY, algorithms=['HS256'])
                        userid = payload['user_id']
                        expire = int(payload['exp'])

                        if payload['token_type'] == "access":
                            # Check token expiration

                            if datetime.fromtimestamp(expire) < datetime.now():
                                return JsonResponse({'error': 'Token has expired'}, status=401)

                            # Attach the user to the request
                            user = CustomUser.objects.filter(id=userid).first()
                            if user is not None:
                                request.user = user
                                request.user_id = user.id
                            else:
                                return JsonResponse({'error': 'User not found'}, status=401)
                            response = self.get_response(request)
                            return response
                        else:
                            return JsonResponse({'error': 'Provide a valid access token'}, status=401)
                    # except jwt.ExpiredSignatureError:
                    #     return JsonResponse({'error': 'Token has expired'}, status=401)
                    # except jwt.InvalidTokenError:
                    #     return JsonResponse({'error': 'Invalid token'}, status=401)
                else:
                    return JsonResponse({'error': 'Provide valid credentials'}, status=401)
            else:
                return JsonResponse({'error': 'Auth token not provided'}, status=401)
        except Exception as e:
            # Handle unexpected exceptions
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)