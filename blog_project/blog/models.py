from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
# Create your models here.

# Model cho người dùng (User)
class User(AbstractUser):
    # Thêm trường role
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('editor', 'Editor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Thêm trường description
    description = models.TextField(default='This is a user description.')

    # Thêm trường image
    image = models.ImageField(upload_to='user_images/', default='#')

    def __str__(self):
        return self.username

    
# Model cho thẻ (Tag) của bài viết
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
# Model cho danh mục (Category) của bài viết
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='This is a category description.')
    image = models.ImageField(upload_to='category_images/', default='#')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    
# Model cho bài viết (Post)
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/')  # Trường hình ảnh
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Để chỉ trạng thái công khai hoặc ẩn
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title

# Model cho bình luận (Comment) trên bài viết
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content
    
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} likes {self.comment}"

    class Meta:
        unique_together = ('user', 'comment')