from django.db import models
from core.models import Orders, Product

# Create your models here.
class users(models.Model):
    image = models.ImageField(upload_to="consumer/", null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    contact = models.IntegerField(unique=True, null=True, blank=True)
    sessionID = models.CharField(max_length=36, null=True, blank=True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    createOn = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)


    order = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class cart(models.Model):
    price = models.IntegerField()
    products = models.ForeignKey(Product, on_delete=models.CASCADE)