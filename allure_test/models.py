import uuid
from django.db import models


class Product(models.Model):
    UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    price = models.IntegerField()
    is_published = models.BooleanField()
    last_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
