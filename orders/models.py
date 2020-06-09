from django.db import models

# Create your models here.
from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
    shipping_total = models.DecimalField(decimal_places=2, max_digits=100, default=5.00)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)

    def __str__(self):
        return self.order_id
