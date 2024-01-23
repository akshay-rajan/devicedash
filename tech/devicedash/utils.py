from asgiref.sync import sync_to_async
from .models import Brands, Phones, Specifications

def saveBrand(brand_id, brand_name):
    brand_data = Brands(brand_id=brand_id, brand=brand_name)
    brand_data.save()
    
def saveDevice(brand_id, device_id, device_name):
    brand = Brands.objects.get(brand_id=brand_id)
    device_data = Phones(brand=brand, device_id=device_id, name=device_name)
    device_data.save()
    
def saveSpecs(device_id, img, quick_spec, detail_spec, pricing, popularity):
    device = Phones.objects.get(device_id=device_id)
    specs = Specifications(device=device, img=img, quick_spec=quick_spec, pricing=pricing, popularity=popularity)
    specs.save()

# Wrap the synchronous function for asynchronous use
async_saveBrand = sync_to_async(saveBrand)
async_saveDevice = sync_to_async(saveDevice)
async_saveSpecs = sync_to_async(saveSpecs)
