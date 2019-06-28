from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return "Warehouse of " + self.name + " is in: " + self.warehouse


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    intrested = models.PositiveIntegerField(default=0)

    def refill(self):
        self.stock+=100

    def __str__(self):
        return self.name + ": has stock of " + str(self.stock)


class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec')]
    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    profile_image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Order(models.Model):
    ORDER_CHOICES = [(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'Order Shipped'), (3, 'Order Delivered')]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=100)
    order_status = models.IntegerField(max_length=1, choices=ORDER_CHOICES, default=1)
    status_date = models.DateField(default=timezone.now)

    def total_cost(self):
        return self.product.price * self.num_units

    def __str__(self):
        return 'Order# ' + str(self.id) + ': ' + str(self.num_units) + " " + self.product.name + "(s) " + "by " + str(self.client) + " >> Total Amount Paid: " + str(self.total_cost())


