from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime,date
from blog_app.models import Article, Comment


class CheckTitle:
    def __call__(self, value):
        if value == "html":
            raise serializers.ValidationError({"title":"title can not be html"})

def check_title(data):
    if data["title"] == "html":
        raise serializers.ValidationError({"title":"title can not be html"})


#using model serializer
class CommentSerializer(serializers.ModelSerializer):
    days_ago = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ("id","text","days_ago")


    def get_days_ago(self, obj):
        return (now().date()-obj.created_at.date()).days


class ArticleSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(validators=[CheckTitle()])
    # text = serializers.CharField()
    # status = serializers.BooleanField()
    comments = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def get_comments(self, obj):
        serializer = CommentSerializer(instance=obj.comments.all(), many=True)
        return serializer.data




# class ArticleSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(write_only=True)
#     comments = serializers.SerializerMethodField()
#     user = serializers.SlugRelatedField(slug_field='last_name', read_only=True)
#     user = serializers.StringRelatedField(read_only=True)
#
#     class Meta:
#         model = Article
#         fields = ("id","title","text","status","user","comments")
#         read_only_fields = ["id"]
#         validators = [CheckTitle()]
#
#     def get_user(self, obj):
#         return obj.user.username
#
#     def validate_title(self, value):
#          if value == "html":
#              raise serializers.ValidationError("html is not correct")
#          return value
#
#     def validate(self, attrs):
#          if attrs["title"]==attrs["text"]:
#              raise serializers.ValidationError("title and text are same")
#          return attrs
#
#
#     def get_comments(self,obj):
#         serializer = CommentSerializer(instance=obj.comments.all(), many=True)
#         return serializer.data
#
#     def create(self, validated_data):
#         request = self.context.get("request")
#         validated_data["user"] = request.user
#         return Article.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    articles  = serializers.PrimaryKeyRelatedField(read_only=True,many=True)
    class Meta:
        model = User
        fields = ("id","username","email","password","articles")