from .views import *
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refreshtoken'),
    path("update/customer/", update_customer, name="update_customer"),
    
    path("ads/", ads, name="ads"), 
    path("ads/<int:pk>/", ads, name="ad"),

    path("cars/<int:pk>/", cars, name="get_my_car"),
    path("cars/", cars, name="get_my_cars"),
]
