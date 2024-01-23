from asgiref.sync import sync_to_async
from .models import Brands, Phones, Specifications

def saveBrand(brand_id, brand_name):
    brand_data = Brands(brand_id=brand_id, brand=brand_name)
    brand_data.save()
    
def saveDevice(brand_id, device_id, device_name):
    brand = Brands.objects.get(brand_id=brand_id)
    device_data = Phones(brand=brand, device_id=device_id, name=device_name)
    device_data.save()

# Wrap the synchronous function for asynchronous use
async_saveBrand = sync_to_async(saveBrand)
async_saveDevice = sync_to_async(saveDevice)
