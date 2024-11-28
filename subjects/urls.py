# accounts/urls.py
from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('<code>/', views.subject_detail, name='subject-detail'),
    path('<code>/lessons/', views.subject_lessons, name='subject-lessons'),
    path('<code>/lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('<code>/lessons/<int:pk>/add', views.add_lesson, name='add-lesson'),
    path('<code>/lessons/<int:pk>/edit', views.edit_lesson, name='edit-lesson'),
    path('<code>/lessons/<int:pk>/delete', views.delete_lesson, name='delete-lesson'),
    path('<code>/marks/', views.mark_list, name='mark-list'),
    path('<code>/marks/edit/', views.edit_marks, name='edit-marks'),
]
