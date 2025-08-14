from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main.forms import CustomLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),

    # Вход/выход (LoginView/LogoutView — готовые вьюхи Django)
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='main/login.html',
            authentication_form=CustomLoginForm
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Твои маршруты приложения
    path('', include('main.urls')),
]
