from django.db import models

# Create your models here.
class TwitterAccounts(models.Model):
    tlink = models.CharField(max_length=200)