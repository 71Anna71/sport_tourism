"""
URL configuration for sport_tourism project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# sport_tourism/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from board import views as board_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),  # Все адреса из приложения board
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path( 'accounts/logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('accounts/signup/', board_views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)