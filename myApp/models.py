from django.db import models


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

