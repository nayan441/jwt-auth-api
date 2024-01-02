from django.urls import path
from .views import UserListCreateView, BlogListCreateAPIView
from .views import (login_view, generate_access_token_view,
                    revoke_refresh_token_view, )

urlpatterns = [
    path('register/', UserListCreateView.as_view(), name='register'),

    path('token/', login_view, name='token_obtain_pair'),
    path('token/refresh/', generate_access_token_view, name='token_refresh'),
    path('token/revoke/', revoke_refresh_token_view, name='token_revoke'),

    path('blogs/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogListCreateAPIView.as_view(), name='blog-detail'),
]
