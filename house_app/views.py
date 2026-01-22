from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    UserProfile,
    Region,
    City,
    District,
    Property,
    Review
)

from .serializers import (
    UserProfileSerializer,
    RegionSerializer,
    CitySerializer,
    DistrictSerializer,
    PropertySerializer,
    PropertyCreateSerializer,
    ReviewSerializer
)
