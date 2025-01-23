from django.contrib import admin
from .models import Article,BlockUser,Comment
# Register your models here.
admin.site.register(Article)
admin.site.register(BlockUser)
admin.site.register(Comment)