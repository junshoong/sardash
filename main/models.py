from django.db import models

# Create your models here.

class Server(models.Model):
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=30, blank=True, null=True)
