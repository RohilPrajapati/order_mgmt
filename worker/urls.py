from django.urls import path,include
from .views import HelloWorld
urlpatterns = [
    path('',HelloWorld.as_view(),name="hello_world"),
]
