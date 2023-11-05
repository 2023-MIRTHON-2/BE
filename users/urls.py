from django.urls import path
from .views import *

urlpatterns = [
    path('checklicense/<str:license_number>/', CheckLicenseView.as_view()),

    #path('dj/signup/<str:registration_type>/', CustomRegisterView.as_view(), name='custom_register'),
]