from django.urls import path
from .views import *

urlpatterns = [
    path('checklicense/<str:license_number>/', CheckLicenseView.as_view()),

]

#dkdk
