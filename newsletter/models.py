from django.db import models


# Create your models here.
class Newsletter(models.Model):
    email = models.EmailField(unique=True, default=None)
