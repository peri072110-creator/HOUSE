
from rest_framework import viewsets, permissions
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

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.prefetch_related(
        'cities__districts'
    )
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = City.objects.all()
        region_id = self.request.query_params.get('region')

        if region_id:
            queryset = queryset.filter(region_id=region_id)

        return queryset

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = District.objects.all()
        city_id = self.request.query_params.get('city')

        if city_id:
            queryset = queryset.filter(city_id=city_id)

        return queryset

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.select_related(
        'region',
        'city',
        'district',
        'seller'
    ).prefetch_related(
        'images',
        'documents'
    )

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = [
        'region',
        'city',
        'district',
        'property_type'
    ]

    search_fields = [
        'title',
        'description',
        'address'
    ]

    ordering_fields = [
        'price',
        'area',
        'created_at'
    ]

    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PropertyCreateSerializer
        return PropertySerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.select_related(
            'author',
            'seller'
        )

        seller_id = self.request.query_params.get('seller')
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)