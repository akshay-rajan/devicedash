from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import asyncio

from .scrape import getDevice, getDataFromUrl, getDevices

def index(request):
    """Render the homepage"""
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
