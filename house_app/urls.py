from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileViewSet,
    RegionViewSet,
    CityViewSet,
    DistrictViewSet,
    PropertyViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'regions', RegionViewSet, basename='regions')
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'districts', DistrictViewSet, basename='districts')
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]