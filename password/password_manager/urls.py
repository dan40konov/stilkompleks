from django.urls import path
from . import views 

urlpatterns = [
    path('accounts_list/', views.accounts_list, name='accounts_list'),  
    path('add_account/', views.add_account, name='add_account'), 
    path('view_pass/<int:pk>/', views.view_pass, name='view_pass'),
    path('update_details/<int:pk>/', views.update, name='update_details'),
    path('delete/<int:pk>/', views.delete, name='delete'),


]