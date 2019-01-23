from django.db import models

# Create your models here.
class homepage(models.Model):
    image = models.ImageField(upload_to='img/')


