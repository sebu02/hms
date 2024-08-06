from django.urls import path

from app1.api.v1.views import app1views
from app1.api.v1.views.app1views import *
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)


urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('doctors/',DoctorView.as_view(),name='doctor-view'),
    path('doctors/<int:pk>',doctor_profile_view,name='doctor-profile-view'),
    path('patient/',PatientView.as_view(),name='patient-view'),
    path('patient/<int:pk>',patient_profile_view,name='patient-profile-view'),
    path('patient_records/',PatientRecordView.as_view(),name='patient-record=view'),
    
    
   
    
]