from django.urls import path
from .views import *
urlpatterns = [
    path('', ProductCreate.as_view()),
    path('rud/<int:pk>/', ProductRetUpDel.as_view())
]