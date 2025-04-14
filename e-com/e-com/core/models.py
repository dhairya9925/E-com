from django.db import models
from seller.models import Seller

# Create your models here.
class countryCode(models.Model):
    country = models.CharField(max_length=100)
    dialCode = models.CharField(max_length=5)
    image = models.CharField(max_length=100)
    def __str__(self):
        return self.country
    
class Product(models.Model):
    categories = [
        ("Toys"),
        ("Electronics"),
        ("Fashion"),
        ("Beauty And Personal Care"),
        ("Home And Furniture"),
        ("Sports And Outdoors"),
        ("Books And Stationery"),
        ("Food And Beverages"),
        ("Health And Medical"),
        ("Automotive And Tools"),
        ("Pet Supplies"),
        ("Office Products"),
        ("Arts And Crafts"),
        ("Baby And Kids"),
        ("Luxury And Designer"),
        ("Books Music And Movies"),
        ("Seasonal Products"),
        ("Travel And Luggage"),
        ("Digital Products"),
        ("Gifts And Special Occasion"),
        ("Sustainability And Eco Friendly")
    ]
    
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=16)
    price = models.IntegerField()
    stock = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=50)
    addedOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name
    

class Orders(models.Model):
    status = [
        ("p", "pending") ,
        ("s", "shipped") ,
        ("d", "delivered") ,
        ("c", "canceled") ,
    ]
    price = models.IntegerField()
    quantity = models.IntegerField()
    orderOn = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField( max_length=1, choices=status, default='p')
    totalItems = models.IntegerField()

    # buyer = models.ForeignKey(users, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.id

