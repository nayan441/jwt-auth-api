from django.contrib import admin
from .models import CustomUser, Blog, BlacklistedRefreshToken, OutstandingRefreshToken

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Blog)
admin.site.register(BlacklistedRefreshToken)
admin.site.register(OutstandingRefreshToken)
