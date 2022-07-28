from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone

from store.models import Store
from store.utils import create_slug


class ProductManager(models.Manager):

    def active_products(self):
        # get list of active products ( Product to be shown)
        return self.filter(is_active=True, uploaded_date__lte=timezone.now())

    def in_active_products(self):
        # get list of inactive products (Based on sold out or not shown yet)
        return self.filter(is_active=False, uploaded_date__lte=timezone.now())


class Product(models.Model):
    """
    uploaded date is the date the item should be uploaded
    """
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    uploaded_date = models.DateField(default=timezone.now)
    view_count = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ProductManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Name: {self.name} --Active: {self.is_active} --View-Count: {self.view_count}"

    @property
    def imageURL(self):
        try:
            if self.image:
                return self.image.url
        except:
            return None

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={
            'slug': self.slug
        })

    def get_update_url(self):
        return reverse("products:product_update", kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse("products:product_delete", kwargs={
            'pk': self.id
        })

    @property
    def real_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance, Product)


pre_save.connect(pre_save_post_receiver, sender=Product)
