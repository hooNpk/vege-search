from django.contrib import admin
from .models import Post, Comment, Restaurant

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Restaurant)