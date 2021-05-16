from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


app_name = 'api'

urlpatterns = [
    path('', views.apiOverview, name='home-api'),
    path('task-list/', views.taskList, name='task-list'),
    path('task-detail/<str:pk>/', views.taskDetail, name='task-detail'),
    path('task-create/', views.taskCreate, name='task-create'),
    path('task-update/<str:pk>/', views.taskUpdate, name='task-update'),
    path('task-delete/<str:pk>/', views.taskDelete, name='task-delete'),

]
