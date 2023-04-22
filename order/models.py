from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Order(models.Model):
    PROCESSING = 'В сборке'
    SHIPPED = 'Отправлен'

    STATUS_CHOICES = (
        (PROCESSING , 'В сборке'),
        (SHIPPED, 'Отправлен'),
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)
    class Meta:
        ordering = ['-created_at',]


    def __str__(self):
        return '%s' % self.id
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id