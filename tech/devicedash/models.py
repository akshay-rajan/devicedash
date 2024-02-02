from django.db import models

class Brands(models.Model):
    brand_id = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.brand} ({self.brand_id})"

class Phones(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"
    
class Specifications(models.Model):
    device = models.OneToOneField(Phones, on_delete=models.CASCADE) 
    img = models.CharField(max_length=255)
    quick_spec = models.JSONField(null=True, blank=True)
    pricing = models.JSONField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.device.name}"