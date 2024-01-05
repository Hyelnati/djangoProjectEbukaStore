from django.db import models

# Create your models here.

from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from django.conf import settings


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey("Collection", on_delete=models.CASCADE, related_name='products')
    # cart = models.ManyToManyRel("Product")  # many to many relationship between cart and product


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Cart(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('C','COMPLETED'),
        ('P','PENDING'),
        ('F','FAILED'),
    ]
    order_id = models.UUIDField(default=uuid4, primary_key=True)  # TO SPECIFY TO DJANGO YOUR OWN PRIMARY KEY
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='P')
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Customer(models.Model):
    MEMBERSHIP_CHOICE = [
        ('G','GOLD'),
        ('B','BRONZE',),
        ('S','SILVER',),
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Address(models.Model):
    house_number = models.PositiveIntegerField()
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
