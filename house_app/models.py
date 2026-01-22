from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )

    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


    def __str__(self):
        return self.username



class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='cities'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.region})'


class District(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.city})'



class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
        ('studio', 'Studio'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='properties_region'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='properties_city'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name='properties_district',
        blank=True,
        null=True
    )

    address = models.CharField(max_length=255)

    area = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    rooms = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()

    seller = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='properties_seller'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='property/images/')

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyDocument(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField(upload_to='property/documents/')


class Review(models.Model):

    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    seller = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} ⭐ from {self.author}'
