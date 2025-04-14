from django.db import models

# Create your models here.

class Seller(models.Model):
    image = models.ImageField(upload_to="seller/", null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    dialCode = models.CharField(max_length=5)
    contact = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    sessionID = models.CharField(max_length=36, null=True, blank=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    companyName = models.CharField(max_length=50)
    gstin = models.CharField(max_length=15)
    storeName = models.CharField(max_length=50)
    createOn = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

