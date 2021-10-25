import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# product category function
class Category(models.Model):
    category = models.CharField(max_length=55, default='Uncategory')
    image = models.ImageField(null=True, blank=True, upload_to='cat_image')

    def __str__(self):
        return self.category


# product information function
class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=2250)
    image = models.ImageField(null=True, blank=True, upload_to='media')
    sale_price = models.FloatField(default=0.00)
    asking_price = models.FloatField(null=True, default=0.00)
    cat = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# product image gallery function
class Gallery(models.Model):
    images = models.ImageField(null=True, blank=True, upload_to='gallery')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


# product Cart function
class CartItem(models.Model):
    quantity = models.IntegerField(default=1)
    item = models.IntegerField(default=1)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    option = models.BooleanField(default=True)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


# cupon function
class Cupon(models.Model):
    CHOICE = (
        ("Fixed", "Fixed"),
        ("Percentage", "Percentage"),
    )
    code = models.CharField(max_length=30, default="Cup25")
    amount = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=CHOICE)
    min_spend = models.IntegerField(default=0)

    def __str__(self):
        return self.code


# discounted price
class Discount(models.Model):
    cupon_code = models.ForeignKey(Cupon, null=True, blank=True, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    discount = models.FloatField(default=0)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)


# customers orders
class Order(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_total = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    shipping = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
