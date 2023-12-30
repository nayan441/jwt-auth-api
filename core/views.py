
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class BlogListCreateAPIView(APIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"{e}"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            request.data['user']= request.user.id
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"},status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request,pk):
        try:
            blog = Blog.objects.filter(id=int(pk)).first()
            if blog.user != self.request.user:
                return Response({"detail": "You don't have permission to update this blog"}, status=status.HTTP_403_FORBIDDEN)
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):

                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            blog = Blog.objects.filter(id=int(pk)).first()
            if blog.user != self.request.user:
                return Response({"detail": "You don't have permission to update this blog"}, status=status.HTTP_403_FORBIDDEN)
            blog.delete()
            return Response({"detail": "Object got successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": f"{e}"},status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print("Received credentials:", request.data.get('username'), request.data.get('password'))
        response = super().post(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            print("Login failed. Response:", response.data)
        return response

class TokenRefreshView(TokenRefreshView):
    pass
class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    def has_delete_permission(self, *args, **kwargs):
        return True
    


class UserTokenRevokeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Tokens revoked successfully.'}, status=status.HTTP_200_OK)
        
            except Exception as e:
                return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Refresh token is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)