from . import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from board.forms import ВходForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Главная страница
    path('add/', views.add_ad, name='add_ad'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:pk>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('my_ads/', views.my_ads, name='my_ads'),
    path('ad/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('ad/<int:pk>/inactive/', views.mark_inactive, name='mark_inactive'),
    path('admin/users/', views.all_users, name='all_users'),
    path('users/', views.all_users, name='all_users'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),


]

