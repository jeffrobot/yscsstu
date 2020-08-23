from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepage, name="homepage"),
    path('yblog/register/',views.register, name="register"),
    path('yblog/login/', views.login_request, name="login"),
    path('yblog/logout/', views.logout_request, name="logout"),
    path('yblog/new/', views.post_new, name="post_new"),
    path('yblog/<int:pk>/detail/', views.post_detail, name="post_detail"),
    path('yblog/<int:pk>/edit/', views.post_edit, name="post_edit"),
    path('yblog/<int:pk>/delete/', views.post_delete, name="post_delete"),
    path('yblog/search/', views.post_search, name="post_search"),
    path('yblog/<int:pk>/comment/', views.add_comment, name="add_comment"),
    path('yblog/<int:pk>/approve/',views.comment_approve, name="comment_approve"),
    path('yblog/<int:pk>/remove/',views.comment_remove, name="comment_remove"),
    path('yblog/study/',views.study_post, name="study_post"),
    path('yblog/clubs/', views.clubs_post, name="clubs_post"),
    path('yblog/notice/',views.notice_post, name="notice_post"),
    path('yblog/social/', views.social_post, name="social_post"),
    path('yblog/all/', views.post_all, name="post_all"),
    path('yblog/<int:pk>/preference/<int:userpreference>/', views.post_preference, name="post_preference"),
    path('yblog/my_page/',views.my_page, name="my_page")
]