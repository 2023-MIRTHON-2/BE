from django.urls import path
from .views import FilterPlaceListView, MakePlaceView


app_name = 'places'

urlpatterns = [
    path('<str:location>/<str:category>/', FilterPlaceListView.as_view()),
    path('make/', MakePlaceView.as_view()),

]