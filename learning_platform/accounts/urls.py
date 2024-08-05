from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', CreateView.as_view(template_name='accounts/register.html', form_class=CustomUserCreationForm), name='register'),
]
