from django.urls import path
from .views import UserCreateView, UserListView
from .views import (UserCreateView, ObtainTokenPairView, TokenRefreshView,
                                    BlogListCreateAPIView,UserTokenRevokeView)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('all/', UserListView.as_view(), name='all'),

    path('token/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/revoke/', UserTokenRevokeView.as_view(), name='token_revoke'),

    path('blogs/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogListCreateAPIView.as_view(), name='blog-detail'),
]
