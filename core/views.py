from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, BlacklistedToken,OutstandingToken
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.filter(user=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk, user=self.request.user)
        except Blog.DoesNotExist:
            return None

    def get(self, request, pk):
        blog = self.get_object(pk)
        if blog:
            serializer = BlogSerializer(blog)
            return Response(serializer.data)
        return Response({"detail": "Blog not found or you don't have permission to access"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        blog = self.get_object(pk)
        if blog:
            serializer = BlogSerializer(blog, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Blog not found or you don't have permission to update"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        if blog:
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Blog not found or you don't have permission to delete"}, status=status.HTTP_404_NOT_FOUND)



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
        token = RefreshToken(refresh_token)
        print("refresh_token  " + refresh_token)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'detail': 'Tokens revoked successfully.'}, status=status.HTTP_200_OK)
        
            except Exception as e:
                return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Refresh token is required in the request body.'}, status=status.HTTP_400_BAD_REQUEST)