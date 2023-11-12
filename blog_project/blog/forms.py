from django import forms
from .models import Comment, Post, User, Category, Tag
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'description', 'image']
        widgets = {
            'password': forms.PasswordInput()
        }


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Chỉ cho phép người dùng nhập nội dung bình luận

        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            self.fields['content'].widget.attrs.update({'class': 'custom-comment-content'})


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  
        required=False, # Không bắt buộc phải chọn
        widget=forms.CheckboxSelectMultiple
    )
    class Meta: 
        model = Post
        fields = ['title', 'content', 'image', 'status', 'category', 'tags',] # Chọn các trường dữ liệu bạn muốn cho phép người dùng chỉnh sửa
   

class CategoryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), # Lấy tất cả các thẻ
        required=False, # Không bắt buộc phải chọn
        widget=forms.CheckboxSelectMultiple, # Hiển thị dưới dạng checkboxes
    )
    class Meta: 
        model = Category
        fields = ['name', 'description', 'image', 'tags'] # Chọn các trường dữ liệu bạn muốn cho phép người dùng chỉnh sửa

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
