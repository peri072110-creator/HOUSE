from rest_framework import generics, viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response


from .models import UserProfile, Region, City, District, Property, Review
from .serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    RegionSerializer,
    CitySerializer,
    DistrictSerializer,
    PropertySerializer,
    PropertyCreateSerializer,
    ReviewSerializer
)
from .permissions import IsAdmin, IsHost, IsGuest, IsOwnerOrAdmin, IsAuthenticated
from .pagination import PropertyPageNumberPagination
from .filters import PropertyFilterSet



class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]
class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.prefetch_related('cities__districts')
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['name']

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



class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.select_related('region', 'city', 'district', 'seller').prefetch_related('images', 'documents')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PropertyPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = PropertyFilterSet
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']


class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.select_related('region', 'city', 'district', 'seller').prefetch_related('images', 'documents')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]


class PropertyCreateView(generics.CreateAPIView):
    serializer_class = PropertyCreateSerializer
    permission_classes = [IsHost | IsAdmin]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class PropertyUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializer
    permission_classes = [IsOwnerOrAdmin]




class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Review.objects.select_related('author', 'seller')
        seller_id = self.request.query_params.get('seller')
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
        return queryset


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsGuest]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
