# middleware.py

from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from .jwt_auth import refresh_access_token, blacklist_refresh_token

class CustomJWTAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        # Override the default behavior to handle token refresh
        user, _ = super().authenticate_credentials(payload)

        # Check if the token is a refresh token
        if payload.get('token_type') == 'refresh':
            # Check if the refresh token is blacklisted
            if self.is_refresh_token_blacklisted(payload['jti']):
                return None

        return user

    def is_refresh_token_blacklisted(self, jti):
        # Implement logic to check if the refresh token is blacklisted
        # This can be done by querying a database table, cache, or any other storage mechanism
        # Return True if the token is blacklisted, otherwise False
        return False
