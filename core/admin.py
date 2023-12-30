from django.contrib import admin
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistedToken,OutstandingToken
from .models import CustomUser, Blog
from .views import CustomOutstandingTokenAdmin
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)