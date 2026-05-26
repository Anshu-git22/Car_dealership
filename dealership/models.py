from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def is_buyer(self):
        return self.user_type == 'buyer'

    def is_seller(self):
        return self.user_type == 'seller'

    def __str__(self):
        return self.username
    
class Car(models.Model):

    seller = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    brand = models.CharField(max_length=100)

    model_name = models.CharField(max_length=100)

    year = models.IntegerField()

    fuel_type = models.CharField(max_length=50)

    transmission = models.CharField(max_length=50)

    engine = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=12, decimal_places=2)

    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)

    kilometers_driven = models.IntegerField()

    description = models.TextField()

    image = models.ImageField(upload_to='cars/')

    city = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} {self.model_name}"
    
class Booking(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
    )

    buyer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE
    )

    booking_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.buyer.username} booked {self.car.brand}"
    
    STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Rejected', 'Rejected'),
)
    
class Wishlist(models.Model):

    buyer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} - {self.car.model_name}"