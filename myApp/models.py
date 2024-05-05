from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(default=0.0)
    description = models.TextField()
    compositon = models.TimeField(default='')
    prodapp = models.TextField(default='')
    product_image = models.ImageField(upload_to='products',default='/myApp/static/product/redrose.jpg') 

    def __str__(self):
        return self.title
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_ref = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart item for {self.user.username}: {self.product_ref}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=10)