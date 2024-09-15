from django.db import models

# Create your models here.

class Plant(models.Model):
    plant = models.ImageField(upload_to='plants/', null=False, blank=False)
    species = models.CharField(max_length=100, null=False, blank=False)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.species}"