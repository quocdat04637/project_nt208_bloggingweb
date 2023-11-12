from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category, Tag, User, CommentLike
from .forms import UserProfileForm, CommentForm, PostForm, RegistrationForm, LoginForm, CategoryForm, TagForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
def base(request):
    categories = Category.objects.all()
    return render(request, 'blog/base.html', {'categories': categories,})

def home(request):
    # Lấy 5 bài đăng mới nhất sắp xếp theo thời gian tạo giảm dần
    new_posts = Post.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    # Truyền danh sách bài đăng vào template
    context = {
        'new_posts': new_posts,
        'categories': categories,
        'tags': tags,
    }
    # Sử dụng template để render trang chủ và trả về HttpResponse
    return render(request, 'blog/home.html', context)


def post_list(request):
    # Logic để lấy danh sách bài viết từ CSDL và hiển thị lên trang web
    posts  = Post.objects.order_by('-created_at')
    authors = User.objects.filter(role='editor')
    categories = Category.objects.all()

    # Xử lý tham số truy vấn
    filter_author = request.GET.get('filter_author')
    filter_category = request.GET.get('filter_category')
    filter_date = request.GET.get('filter_date')

    if filter_author:
        # Lọc theo tác giả nếu filter_author có giá trị
        posts = posts.filter(author__id=filter_author)
    if filter_category:
        # Lọc theo thể loại nếu filter_category có giá trị
        posts = posts.filter(category__id=filter_category)
    if filter_date:
        # Lọc theo ngày đăng nếu filter_date có giá trị
        posts = posts.filter(created_at__date=filter_date)

    return render(request, 'blog/post_list.html', {'posts': posts, 'authors': authors,'categories': categories,})

 
def post_detail(request, pk):
    # Logic để hiển thị chi tiết bài viết và bình luận
    post = get_object_or_404(Post, pk=pk)
    post_author = User.objects.filter(username=post.author)
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    # Get the tags associated with the current post
    post_tags = post.tags.all()

    # Kiểm tra xem người dùng hiện tại đã "like" Comment hay chưa
    user_likes = {}
    if request.user.is_authenticated:
        for comment in comments:
            user_likes[comment.pk] = CommentLike.objects.filter(user=request.user, comment=comment).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Xử lý bình luận mới nêú có
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user  # Gán người dùng hiện tại là tác giả của bình luận
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            # Hiển thị thông báo lỗi nếu người dùng chưa đăng nhập
            messages.error(request, 'Bạn cần đăng nhập để bình luận.')
            return render(request, 'blog/post_comment_error.html', {'post': post, 'comments': comments,})
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'related_posts': related_posts, 'post_tags': post_tags, 'post_author': post_author, 'user_likes': user_likes,})


# Sử dụng form PostForm trong view để tạo bài viết mới hoặc chỉnh sửa bài viết
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = datetime.now()
            post.save()
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def delete_post(request, pk):
    # Lấy bài viết cần xoá từ CSDL hoặc trả về lỗi 404 nếu không tồn tại
    post = get_object_or_404(Post, pk=pk)

    # Kiểm tra quyền truy cập: chỉ người tạo bài viết mới được xoá
    if request.user == post.author:
        if request.method == 'POST':
            # Xoá bài viết nếu người dùng xác nhận xoá
            post.delete()
            return redirect('post_list')
        else:
            # Hiển thị trang xác nhận xoá bài viết
            return render(request, 'blog/post_confirm_delete.html', {'post': post})
    else:
        # Trả về lỗi 403 nếu không có quyền xoá
        return render(request, 'blog/post_delete_permission_denied.html')
    
    
def edit_post(request, pk):
    # Lấy bài viết cần chỉnh sửa từ CSDL hoặc trả về lỗi 404 nếu không tồn tại
    post = get_object_or_404(Post, pk=pk)

    # Kiểm tra quyền truy cập: chỉ người tạo bài viết mới được chỉnh sửa
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.updated_at = datetime.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        # Trả về lỗi 403 nếu không có quyền chỉnh sửa
        return render(request, 'blog/post_edit_permission_denied.html')
    
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # Lấy danh sách bài viết thuộc thể loại này
    posts = category.post_set.all()
    return render(request, 'blog/category_detail.html', {'posts': posts, 'category': category})

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    # Lấy danh sách bài viết liên quan đến tag này
    posts = tag.post_set.all()
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'posts': posts})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'comment_form': comment_form})


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'blog/comment_list.html', {'comments': comments})

def delete_comment(request, pk):
    # Lấy comment cần xoá từ CSDL hoặc trả về lỗi 404 nếu không tồn tại
    comment = get_object_or_404(Comment, pk=pk)
    # Kiểm tra quyền truy cập: chỉ người tạo comment hoặc admin mới được xoá
    if request.user == comment.user or request.user.is_staff:
        if request.method == 'POST':
            # Xoá comment nếu người dùng xác nhận xoá
            comment.delete()
            return redirect('post_detail', pk=comment.post.pk)
        else:
            # Hiển thị trang xác nhận xoá bài viết
            return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
    else:
        # Trả về lỗi 403 nếu không có quyền xoá
        return render(request, 'blog/comment_delete_permission_denied.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Đăng ký thành công!')
            return redirect('home')
    else:
        form = RegistrationForm()
    # Set a variable to indicate successful registration
    context = {'registration_successful': True, 'form': form}
    return render(request, 'blog/register.html', context)
            

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('home')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
        else:
            messages.error(request, 'Tên đăng nhập và mật khẩu không hợp lệ.')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user  # Lấy thông tin người dùng hiện tại
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            if new_password:
                user.password = make_password(new_password)  # Mã hóa mật khẩu mới
                update_session_auth_hash(request, user)  # Cập nhật session auth hash
            form.save()
            messages.success(request, 'Thông tin đã được cập nhật thành công.')
            return redirect('login')

    else:
        form = UserProfileForm(instance=user)

    return render(request, 'blog/profile.html', {'form': form})



def dashboard_view(request):
    # Lấy người dùng đang đăng nhâp
    user = request.user
    # Lấy tất cả bài viết của người dùng, xếp theo thứ tự mới nhất trước 
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/dashboard.html', {'user_posts': user_posts, 'categories': categories, 'tags': tags,})

def view_time(request):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")  # Format as a string
    return render(request, 'blog/base.html', {'current_time': current_time_str})


def all_posts(request):
    render(request, 'blog/all_posts.html')


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()
    return render(request, 'blog/category_create.html', {'form': form})

def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            # Redirect to the tag detail page after creating the tag
            return redirect('tag_detail', pk=tag.id)
    else:
        form = TagForm()
    return render(request, 'blog/tag_create.html', {'form': form})

def author_detail(request, pk):
    author = get_object_or_404(User, pk=pk)
    # Retrieve posts authored by this author
    author_posts = Post.objects.filter(author=author)
    return render(request, 'blog/author_detail.html', {'author': author, 'author_posts': author_posts})

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    user = request.user

    # Kiểm tra xem người dùng đã "like" bình luận này chưa
    if CommentLike.objects.filter(user=user, comment=comment).exists():
        # Người dùng đã "like" rồi, không thể "like" lại
        return JsonResponse({'message': 'You have already liked this comment.'}, status=400)
    
    # Tăng số lượt "like" của bình luận và lưu lại
    comment.likes += 1
    comment.save()

    # Tạo một bản ghi "like" trong mô hình CommentLike
    CommentLike.objects.create(user=user, comment=comment)

    return JsonResponse({'message': 'Liked successfully', 'likes': comment.likes})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def privacy_policy(request):
    return render(request, 'blog/privacy_policy.html')

def faq(request):
    return render(request, 'blog/faq.html')

def term_of_use(request):
    return render(request, 'blog/term_of_use.html')


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(title__icontains=query)
    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'blog/search_results.html', context)