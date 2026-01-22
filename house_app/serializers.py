from rest_framework import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    UserProfile,
    Region,
    City,
    District,
    Property,
    PropertyImage,
    PropertyDocument,
    Review
)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ( 'first_name',   'username','email', 'password',  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id', 'username',  'email', 'phone_number','role',
        )

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'districts')

class RegionSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'name', 'cities')

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('id', 'image')

class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = ('id', 'file')

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    documents = PropertyDocumentSerializer(many=True, read_only=True)

    region = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    district = serializers.StringRelatedField()

    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'title', 'description', 'property_type', 'region', 'city',
                 'district','address', 'area', 'price',  'rooms','floor','total_floors',
                  'seller', 'images', 'documents', 'created_at',
        )


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'title', 'description','property_type', 'region', 'city','district',
            'address','area', 'price', 'rooms', 'floor', 'total_floors',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['seller'] = request.user

        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'author', 'seller', 'rating', 'comment', 'created_at',
        )
