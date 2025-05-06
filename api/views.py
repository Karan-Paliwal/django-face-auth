from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import BlogPostSerializer
from .models import BlogPost
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def delete(self, request, *args, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]  # Restrict access

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can log out

    def post(self, request):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)