from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    # Đường dẫn đến danh sách bài viết
    path('post_list/', views.post_list, name='post_list'),

    # Đường dẫn đến chi tiết bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>', views.post_detail, name='post_detail'),

    # Đường dẫn để tạo bài viết mới
    path('post/new/', views.create_post, name='create_post'),

    # Đường dẫn để chỉnh sửa bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),

    # Đường dẫn để xoá bài viết với sử dụng số nguyên làm primary key (pk)
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    # Đường dẫn đến trang danh sách các thể loại (categories)
    path('categories/', views.category_list, name='category_list'),

    # Đường dẫn đến trang chi tiết thể loại 
    path('category/<int:pk>/', views.category_detail, name='category_detail'),

    # Đường dẫn đến trang danh sách các tags
    path('tags/', views.tag_list, name='tag_list'),

    # Đường dẫn đến trang chi tiết tag
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),

    # Đường dẫn để tạo bình luận mới cho bài viết
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

    # Đường dẫn đến trang danh sách các bình luận
    path('comments/', views.comment_list, name='comment_list'),

    # Đường dẫn để xoá comment với sử dụng số nguyên làm primary key (pk)
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    path('register/', views.register, name='register'),

    path('login/', views.user_login, name='login'),

    path('profile_view/', views.profile_view, name='profile_view'),

    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('dashboard_view/', views.dashboard_view, name='dashboard_view'),

    # Đường dẫn để tạo Category mới
    path('category/new/', views.create_category, name='create_category'),

    # Đường dẫn để tạo Tag mới
    path('tag/new/', views.create_tag, name='create_tag'),

    path('author/<int:pk>', views.author_detail, name='author_detail'),

    # Đường dẫn để "like" Comment
    path('like_comment/<int:pk>/', views.like_comment, name='like_comment'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

    path('faq/', views.faq, name='faq'),

    path('term-of-use/', views.term_of_use, name='term_of_use'),

    path('search/', views.search, name='search'),

]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)