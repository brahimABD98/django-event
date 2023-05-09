from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('index/', views.index),
    path('index/<str:param>', views.index_param),
    path('affiche/', affiche),
    path('liste/', AfficheGeneric.as_view())
]
