from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Case, When, Value, IntegerField, F, JSONField
from django.db.models.functions import Substr
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import re
import json
import random
from time import sleep
from asgiref.sync import sync_to_async

from .scrape import getDevice, getDataFromUrl, getDevices, getBrand, getBrands
from .models import Brands, Phones, Specifications, Devices
from .utils import async_saveBrand, async_saveDevice, async_saveSpecs, cleanup, clean_brand


def index(request):
    """Render the homepage"""
    
    return render(request, "devicedash/index.html")


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


async def storeData(request):
    """Get the details of all phones from the website and store it to our database"""
    
    brands = ["apple-phones-48", "asus-phones-46", "blackberry-phones-36", "google-phones-107", "honor-phones-121", "htc-phones-45", "huawei-phones-58", "infinix-phones-119", "karbonn-phones-83", "lava-phones-94", "lenovo-phones-73", "lg-phones-20", "micromax-phones-66", "microsoft-phones-64", "motorola-phones-4", "nokia-phones-1", "nothing-phones-128", "oneplus-phones-95", "oppo-phones-82", "realme-phones-118", "samsung-phones-9", "sharp-phones-23", "sony-phones-7", "spice-phones-68", "tecno-phones-120", "vivo-phones-98", "xiaomi-phones-80", "zte-phones-62"]

    for brand_id in brands:
        # await async_saveBrand(brand_id, brand_name)
        
        devices = await getBrand(brand_id)
        for device in devices:
            device_id = device["id"]
            device_name = device["name"]
            await async_saveDevice(brand_id, device_id, device_name)
            
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
        
        
def admin(request):
    """Render Admin Login Page"""
    
    return render(request, "devicedash/admin.html")


def logout_view(request):
    logout(request)
    return render(request, "devicedash/logout.html")


def add(request):
    """Log the user in, render the Add Phone form"""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
    brands = Brands.objects.all()
    return render(request,  "devicedash/add.html", {
        "brands": brands
    })



def save(request):
    """Add a new device to the database"""
    
    if request.method == "POST":
        brand_id = request.POST["brand"]
        brand = Brands.objects.get(brand_id=brand_id)
        name = request.POST["name"]
        device_id = f"{brand_id} {name}"
        device = Phones(brand=brand, name=name, device_id=device_id)
        device.save()
        
        img = request.POST["img"]
        quick_spec = [
            {"name": "Display size", "value": request.POST["screen"]},
            {"name": "Display resolution", "value": request.POST["resolution"]},
            {"name": "Camera pixels", "value": request.POST["pixels"]},
            {"name": "Video pixels", "value": request.POST["video-pixels"]},
            {"name": "RAM size", "value": request.POST["ram"]},
            {"name": "Chipset", "value": request.POST["chipset"]},
            {"name": "Battery size", "value": request.POST["battery"]},
            {"name": "Battery type", "value": request.POST["battery-type"]}
        ]
        price = request.POST["pricing"]
        popularity = request.POST["popularity"]
        specs = Specifications(device=device, img=img, quick_spec=quick_spec, pricing=[price], popularity=popularity)
        specs.save()
        
        dev = Devices(brand=brand, device=device, price=price, popularity=popularity)
        dev.save()        
    
        return render(request, "devicedash/add.html", {
            "brands": Brands.objects.all(),
            "msg": "Saved Successfully!"
        })
        

def all_phones(request):
    """Render a page with the list of all phones"""
    
    phones = []
    phones_list = Phones.objects.all()
    for phone in phones_list:
        phones.append({
            "name": cleanup(phone.name),
            "brand": clean_brand(phone.brand.brand)
        })
    
    paginator = Paginator(phones, 500)
    page = request.GET.get('page')
    try:
        phones = paginator.page(page)
    except PageNotAnInteger:
        phones = paginator.page(1)
    except EmptyPage:
        phones = paginator.page(paginator.num_pages)
    return render(request, "devicedash/all.html", {
        "phones": phones
    })


def search(request):
    """Search through devices by name or brand."""
    
    if request.method == "GET":
        query = request.GET.get("phone")
        phones = Devices.objects.filter(Q(device__name__icontains=query) | Q(brand__brand__icontains=query))
        result = []
        for phone in phones:
            result.append({
                "name": cleanup(phone.device.name),
                "id": phone.device.device_id,
            })
        
        return render(request, "devicedash/results.html", {
            "query": query,
            "phones": result
        })