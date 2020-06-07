from django.db import models
import uuid, os
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
# Create your models here.


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('products', filename)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        return self.slug

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = 'abc'
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)