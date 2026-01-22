from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserListAPIView,
    RegionViewSet,
    CityViewSet,
    DistrictViewSet,
    PropertyListView,
    PropertyDetailView,
    ReviewListView,
    ReviewCreateView,

)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'districts', DistrictViewSet, basename='district')

urlpatterns = [


    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),


    path('users/', UserListAPIView.as_view(), name='user-detail'),


    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),



    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),



]
