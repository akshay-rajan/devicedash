from asgiref.sync import sync_to_async
from .models import Brands

def saveBrand(brand_id, brand_name):
    brand_data = Brands(brand_id=brand_id, brand=brand_name)
    brand_data.save()
    print(brand_id, brand_name)

# Wrap the synchronous function for asynchronous use
async_saveBrand = sync_to_async(saveBrand)
