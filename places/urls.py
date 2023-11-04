from django.urls import path
from views import PlaceListView, LocationPlaceListView


app_name = 'places'

urlpatterns = [
    path('<str:location>/', LocationPlaceListView.as_view()),

]