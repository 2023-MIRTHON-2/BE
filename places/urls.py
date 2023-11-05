from django.urls import path
from .views import *

app_name = 'places'

urlpatterns = [
    path('', MakePlaceListView.as_view()),
    path('<str:category>/<str:location>/', PlaceListView.as_view()),
    path('<int:post_id>/', PlaceDetailView.as_view()),
]