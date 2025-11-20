from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:project_pk>/', views.task_create_view, name='task_create'),
    path('<int:pk>/', views.task_detail_view, name='task_detail'),
    path('<int:pk>/update-status/', views.task_update_status, name='task_update_status'),
    path('<int:task_pk>/comment/', views.comment_create_view, name='comment_create'),
]