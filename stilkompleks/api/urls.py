from django.urls import path
from .views import *

app_name='api'
urlpatterns = [
    path("obekti", ObektiView.as_view()),
    path("create-obekt", CreateObektView.as_view()),
    path("update-obekt", UpdateObektView.as_view()),
    path("delete-obekt/<str:pk>", DeleteObektView.as_view()),
    path("personal", PersonalView.as_view()),
    path("create-personal", CreatePersonalView.as_view()),
    path("update-personal", UpdatePersonalView.as_view()),
    path("delete-personal/<str:pk>", DeletePersonalView.as_view()),
    

]
