from django.contrib import admin
from django.urls import path, include
from courses.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('accounts/', include('accounts.urls')),
]
