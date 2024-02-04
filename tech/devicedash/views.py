from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, Value, IntegerField, F, JSONField
from django.db.models.functions import Substr
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import re
import json
import random
from time import sleep
from asgiref.sync import sync_to_async

from .scrape import getDevice, getDataFromUrl, getDevices, getBrand, getBrands
from .models import Brands, Phones, Specifications, Devices
from .utils import async_saveBrand, async_saveDevice, async_saveSpecs, cleanup


def index(request):
    """Render the homepage"""
    
    return render(request, "devicedash/index.html")

# async def find(request):
#     """Render a page containg the best devices according to the user's price range"""

#     if request.method == "POST":
#         min = request.POST["nPriceMin"]
#         max = request.POST["nPriceMax"]

#         response = await getDataFromUrl(f"/results.php3?nPriceMin={min}&nPriceMax={max}")
#         soup = BeautifulSoup(response, 'html.parser')
#         await asyncio.sleep(1)
#         json_data = []

#         devices = getDevices(soup, soup.select('.makers li'))
#         json_data.extend(devices)
#         json_data = json_data[:10]
#         return render(request, "devicedash/find.html", {
#             "data": json_data,
#         })

def find(request):
    """Render a page containing the best devices according to the price range entered"""
    
            

    if request.method == "GET":
        min_price = request.GET["nPriceMin"]
        max_price = request.GET["nPriceMax"]
        
        # Return the top 10 devices according to popularity within the price range
        devices = Devices.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        ).order_by('-popularity')[:10]
        
        data = []
        for device in devices:
            brand = device.brand
            brand_name = brand.brand
            phone = device.device
            device_name = cleanup(phone.name)
            specs = Specifications.objects.get(device=phone)
            img_url = specs.img
            quick_spec = specs.quick_spec
            
            price = device.price
            popularity = device.popularity
            data.extend([{
                'phone_id': phone.device_id,
                'brand': brand_name,
                'name': device_name,
                'image': img_url,
                'quick_spec': quick_spec,
                'price': price,
                'popularity': popularity
            }])
            
        print(data[:1])
        
        return render(request, "devicedash/find.html", {
            "data": data 
        })

def viewPhone(request, id):
    
    device = Phones.objects.get(device_id=id)
    specs = Specifications.objects.get(device=device)
    brand = device.brand
    other = Devices.objects.get(device=device)
    
    data = {
        "brand": re.sub(r'\d+$', '', brand.brand),
        "name": cleanup(device.name),
        "img": specs.img,
        "quick_spec": specs.quick_spec,
        "price": f"{other.price:.02f}",
        "popularity": other.popularity,        
    }    
    
    return render(request, "devicedash/view.html", {
        "data": data
    })
    

# async def fetchphone(request, id):
#     """Fetch information about a phone"""

#     device_info = await getDevice(id)
#     return JsonResponse(device_info)

async def storeData(request):
    """Get the details of all phones from the website and store it to our database"""
    
    brands = ["apple-phones-48", "asus-phones-46", "blackberry-phones-36", "google-phones-107", "honor-phones-121", "htc-phones-45", "huawei-phones-58", "infinix-phones-119", "karbonn-phones-83", "lava-phones-94", "lenovo-phones-73", "lg-phones-20", "micromax-phones-66", "microsoft-phones-64", "motorola-phones-4", "nokia-phones-1", "nothing-phones-128", "oneplus-phones-95", "oppo-phones-82", "realme-phones-118", "samsung-phones-9", "sharp-phones-23", "sony-phones-7", "spice-phones-68", "tecno-phones-120", "vivo-phones-98", "xiaomi-phones-80", "zte-phones-62"]

    for brand_id in brands:
        # await async_saveBrand(brand_id, brand_name)
        print(brand_id)
        
        devices = await getBrand(brand_id)
        for device in devices:
            device_id = device["id"]
            device_name = device["name"]
            await async_saveDevice(brand_id, device_id, device_name)
            print(brand_id, device_id, device_name)
            
            smartphone = await getDevice(device_id)
            quick_spec = smartphone["quick_spec"]
            img = smartphone["img"]
            pricing = smartphone["pricing"]
            if pricing == '':
                continue
            popularity = smartphone["popularity"]
            try:
                await async_saveSpecs(device_id, img, quick_spec, pricing, popularity)
            except:
                continue
            print(device_id, img, quick_spec, pricing, popularity)
            sleep(random.randint(1, 6))
    
def storeToDevices(request):
    """Store the details of each phone in 'Devices' to access in 'find'"""
    
    def convert_price(item):
        currency = item[1]["price"].split()[0]
        value = float(item[1]["price"].replace(currency, "").replace(",", "").strip())
        if currency == "$":
            return value * 82.9
        return value
        
    
    all_devices = Specifications.objects.all()
    for phone in all_devices:
        device = phone.device
        brand = device.brand
        prices = [convert_price(item) for item in phone.pricing]
        if not prices:
            continue
        price = min(prices)
        popularity = phone.popularity
        try:
            d = Devices(brand=brand, device=device, price=price, popularity=popularity)
            d.save()
        except:
            continue
        
        
