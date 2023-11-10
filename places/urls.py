from django.urls import path
from .views import *

app_name = 'places'

urlpatterns = [
    path('create/', PlaceDetailView.as_view()),
    path('<str:business>/<str:location>/', PlaceListView.as_view()),
    path('<int:place_id>/', PlaceDetailView.as_view()),
    path('checklicense/<str:license_number>/', CheckLicenseView.as_view()),
]
