from django.contrib import admin
from .models import User, Post, Category, Tag, Comment, CommentLike

# Register your models here.
# Đăng ký các mô hình để hiển thị trong Django Admin
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(CommentLike)