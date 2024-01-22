from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import asyncio
import json
from asgiref.sync import sync_to_async

from .scrape import getDevice, getDataFromUrl, getDevices, getBrand, getBrands
from .models import Brands, Phones, Specifications
from .utils import async_saveBrand


async def index(request):
    """Render the homepage"""

    await storeData(request)
    return render(request, "devicedash/index.html")

async def find(request):
    """Render a page containg the best devices according to the user's price range"""

    if request.method == "POST":
        min = request.POST["nPriceMin"]
        max = request.POST["nPriceMax"]

        response = await getDataFromUrl(f"/results.php3?nPriceMin={min}&nPriceMax={max}")
        soup = BeautifulSoup(response, 'html.parser')
        await asyncio.sleep(1)
        json_data = []

        devices = getDevices(soup, soup.select('.makers li'))
        json_data.extend(devices)
        json_data = json_data[:10]
        return render(request, "devicedash/find.html", {
            "data": json_data,
        })


async def fetchphone(request, id):
    """Fetch information about a phone"""

    device_info = await getDevice(id)
    return JsonResponse(device_info)


async def storeData(request):
    """Get the details of all phones from the website and store it to our database"""
    brands = await getBrands()
    for brand in brands:
        brand_id = brand["id"]
        brand_name = brand["name"]
        await async_saveBrand(brand_id, brand_name)
        print(brand_id, brand_name)

        
        # devices = await getBrand(brand_id)
        # for device in devices[:5]:
        #     device_id = device["id"]
        #     device_name = device["name"]
        #     print(brand_id, device_id, device_name)
            
        #     smartphone = await getDevice(device_id)
        #     quick_spec = smartphone["quick_spec"]
        #     detail_spec = smartphone["detail_spec"]
        #     img = smartphone["img"]
        #     pricing = smartphone["pricing"]
        #     popularity = smartphone["popularity"]
        #     print(device_id, img, quick_spec, detail_spec, pricing, popularity)
    