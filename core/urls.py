from django.urls import path
from .views import UserCreateView, UserListView
from .views import (UserCreateView,login_view, generate_access_token_view,
                    revoke_refresh_token_view, BlogListCreateAPIView)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('all/', UserListView.as_view(), name='all'),

    path('token/', login_view, name='token_obtain_pair'),
    path('token/refresh/', generate_access_token_view, name='token_refresh'),
    path('token/revoke/', revoke_refresh_token_view, name='token_revoke'),

    path('blogs/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogListCreateAPIView.as_view(), name='blog-detail'),
]
