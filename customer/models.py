from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    image = models.CharField(max_length=500, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')


    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
    
class OrderModel(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    #order_date = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
