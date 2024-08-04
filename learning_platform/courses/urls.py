from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/add_lesson/', views.create_lesson, name='create_lesson'),
    path('<int:course_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_courses, name='favorite_courses'),
    path('category/<int:category_id>/', views.category_courses, name='category_courses'),
]
