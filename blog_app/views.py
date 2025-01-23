from distutils.command.install import install

from django.contrib.auth.models import User
from django.contrib.staticfiles.views import serve
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import ArticleSerializer, CommentSerializer, UserSerializer
from .models import Article
from .permissions import BlocklistPermission
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import authentication
# Create your views here.
@api_view(['GET','POST'])
def hello_world(request):
    PRO = {
        'NAME':'MILAD',
        'PRICE':576,
    }
    return Response({'message': PRO})

class HelloWorld(APIView):
        def get(self,request):
                name = request.GET.get('name')
                last = request.GET.get('last')
                return Response({'message': f'{name} {last}'})
        def post(self,request):
                return Response({'message': 'Hello post!'})


class ArticleListView(APIView):
        def get(self,request):
                articles = Article.objects.all()
                serilizer = ArticleSerializer(articles,many=True)
                return Response(serilizer.data)

class ArticleDetailView(APIView):
        def get(self,request,pk):
                article = Article.objects.get(pk=pk)
                serilizer = ArticleSerializer(article)
                return Response(serilizer.data)

class ArticleUpdateView(APIView):
    def put (self, request, pk):
        instance = Article.objects.get(id=pk)
        serializer = ArticleSerializer(instance,data=request.data,partial=True)

        if serializer.is_valid():
                serializer.update(instance=instance,validated_data=serializer.validated_data)
                return Response({"responses":"updated"})
        return Response(serializer.errors)

    def delete(self,request,pk):
        instance = Article.objects.get(id=pk)
        instance.delete()
        return Response({"responses":"deleted"})

class AddArticleView(APIView):
    permission_classes = [BlocklistPermission]
    def post(self,request):
        serializer = ArticleSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            instance.status = 1
            instance.save()
            return Response({"responses":"Added"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CheckToken(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        user = request.user
        return Response({'token':user.username},status=status.HTTP_200_OK)

class ArticlesCommentsView(APIView):
    def get(self,request,pk):
        comments = Article.objects.get(id=pk).comments.all()
        serilizer = CommentSerializer(comments,many=True)
        return Response(serilizer.data,status=status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)