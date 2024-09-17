
from django.contrib import admin
from django.urls import path, include
from user import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('register/', user_views.register, name='user-register'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('logout/', user_views.LogoutView, name='user-logout'),
]
