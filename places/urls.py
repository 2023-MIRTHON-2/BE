from django.urls import path
from .views import FilterPlaceListView


app_name = 'places'

urlpatterns = [
    path('<str:location>/<str:category>/', FilterPlaceListView.as_view()),

]