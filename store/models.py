from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse
# Create your models here.
from django.utils import timezone

from store.utils import create_slug


class StoreManager(models.Manager):

    def store_products(self):
        # all store products
        return self.product_set.all()


class Store(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    objects = StoreManager()

    @property
    def products_count(self):
        return self.product_set.count()

    def get_absolute_url(self):
        return reverse("products:store", kwargs={
            'id': self.id
        })

    @property
    def imageURL(self):
        try:
            if self.image:
                return self.image.url
        except:
            return None


def pre_save_store_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance, Store)


pre_save.connect(pre_save_store_receiver, sender=Store)
