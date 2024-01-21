from django.db import models

class Brands(models.Model):
    brand_id = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)

class Phones(models.Model):
    brand_id = models.ForeignKey(Brands, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    
class Specifications(models.Model):
    device_id = models.ForeignKey(Phones, on_delete=models.CASCADE) 
    img = models.ImageField(upload_to='static/phones/', null=True, blank=True)
    quick_spec = models.JSONField(null=True, blank=True)
    detail_spec = models.JSONField(null=True, blank=True)
    pricing = models.JSONField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)