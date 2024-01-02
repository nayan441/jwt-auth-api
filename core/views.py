
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .jwt_auth import create_tokens, refresh_access_token, blacklist_refresh_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListCreateAPIView

class UserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
@method_decorator(csrf_exempt, name='dispatch')
class BlogListCreateAPIView(APIView):

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user= CustomUser.objects.filter(id=request.user_id).first())
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
 
        try:
            user = CustomUser.objects.filter(id=request.user_id).first()
            request.data['user'] = user.id
            serializer = BlogSerializer(data=request.data)
            print(serializer.is_valid()) 
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
            request.data['user']= request.user.id
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


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    tokens = create_tokens(username, password)

    if tokens:
        return Response(tokens, status=200)
    else:
        return Response({'error': 'Failed to create tokens'}, status=500)


@api_view(['POST'])
def generate_access_token_view(request):
    refresh_token = request.data.get('refresh')
    if refresh_token:
        tokens = refresh_access_token(refresh_token)
        if tokens:
            return Response(tokens, status=200)
        else:
            return Response({'error': 'Failed to create access token'}, status=500)
    else:
        return Response({'error': 'Invalid refresh token'}, status=401)
    
@csrf_exempt
@api_view(['POST'])
def revoke_refresh_token_view(request):
    refresh_token = request.data.get('refresh')
    print("refresh_token    " +refresh_token+"\n\n")
    if refresh_token:
        # Create tokens if the user is authenticated
        tokens = blacklist_refresh_token(refresh_token)

        if tokens:
            return Response(tokens, status=200)
        else:
            return Response({'error': 'Failed to revoke token'}, status=500)
    else:
        return Response({'error': 'Invalid refresh token'}, status=401)
    



















