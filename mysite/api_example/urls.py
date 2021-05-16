from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('languages', views.LanguageView)

app_name = 'api_example'

urlpatterns = [
    path('', include(router.urls)),
    #path('task-list/', views.taskList, name='task-list'),
    #path('task-detail/<str:pk>/', views.taskDetail, name='task-detail'),
    #path('task-create/', views.taskCreate, name='task-create'),
    #path('task-update/<str:pk>/', views.taskUpdate, name='task-update'),
    #path('task-delete/<str:pk>/', views.taskDelete, name='task-delete'),
]
