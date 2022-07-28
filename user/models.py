from django.db import models
from django.conf import settings

# Create your models here.
from django.db.models.signals import post_save

COUNTRY_CHOICES = (
    ('NIGERIA', 'NIGERIA'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name='user_profile')
    street_address = models.CharField(max_length=100)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='NIGERIA')
    state = models.CharField(max_length=50)
    apartment_address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return str(f"{self.user} --- {self.get_full_address}")

    @property
    def get_full_address(self):
        try:
            return str(f"{self.country} -- {self.state} -- {self.street_address} -- {self.apartment_address}")
        except:
            return str("")

    class Meta:
        verbose_name_plural = 'UserProfiles'


def user_profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)


post_save.connect(user_profile_receiver, sender=settings.AUTH_USER_MODEL)
