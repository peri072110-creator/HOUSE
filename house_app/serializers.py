from rest_framework import serializers
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
