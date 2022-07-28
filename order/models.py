from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.utils import timezone

from product.models import Product


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    @property
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


OrderState = (
    ('CANCELED', 'CANCELED'),
    ('DELIVERED', 'DELIVERED'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ref_code = models.CharField(max_length=250, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    order_state = models.CharField(max_length=50, choices=OrderState, null=True, blank=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    '''
    1. product added to cart
    2. Update profile (Address
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    '''

    def __str__(self):
        return str(f"{self.user.email} --- {self.ordered} -- {self.order_state} -- {self.ref_code}")

    @property
    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price
        return total

    @property
    def get_total_product_count(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.quantity
        return total
