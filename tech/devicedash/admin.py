from django.contrib import admin
from .models import Brands, Phones, Specifications 

# Register your models here.
admin.site.register(Brands)
admin.site.register(Phones)
admin.site.register(Specifications)