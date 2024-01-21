from django.http import JsonResponse
from bs4 import BeautifulSoup
import httpx


async def getDataFromUrl(url):
    """Return the source of a page"""

    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://www.gsmarena.com{url}')
        # print(response.text[:100])
        return response.text

async def getBrands():
    """Return all brands as json objects in a list"""

    response = await getDataFromUrl('/makers.php3')
    soup = BeautifulSoup(response, 'html.parser')
    json_data = []
    brands = soup.find_all('table')[0].find_all('td')
    for element in brands:
        links = element.find('a')
        spans = element.find('span')
        json_data.append({
            'id': links['href'].replace('.php', ''),
            'name': links.get_text(strip=True).replace(' devices', '').replace('[0-9]', ''),
            'devices': int(spans.get_text(strip=True).replace(' devices', ''), 10),
        })
    return JsonResponse(json_data, safe=False)


def getNextPage(soup):
    """If a 'next page' exists, return it"""

    # Look for an anchor tag with the particular class name
    nextPageUrl = soup.select_one('a.pages-next')
    if nextPageUrl:
        nextPage = nextPageUrl['href']
        if '#' in nextPage:
            return False
        return "/" + nextPage
    return False


def getDevices(soup, devices_list):
    """Return a refined list of devices as json objects"""

    devices = []
    for device in devices_list:
        img = device.find('img')
        name = device.find('span').contents
        fullname = f"{name[0]} {name[-1]}"
        devices.append({
            'id': device.find('a')['href'].replace('.php', ''),
            'name': fullname,
            'img': img['src'],
            'description': img['title'],
        })
    return devices


async def getBrand(brand):
    """Return all devices of a particular brand"""

    response = await getDataFromUrl(f"/{brand}.php")
    soup = BeautifulSoup(response, 'html.parser')
    json_data = []

    devices = getDevices(soup, soup.select('.makers li'))
    json_data.extend(devices)
    # Iterate through all subsequent pages of devices
    while getNextPage(soup):
        nextPageUrl = getNextPage(soup)
        nextPage = await getDataFromUrl(nextPageUrl)
        soup = BeautifulSoup(nextPage, 'html.parser')
        devices = getDevices(soup, soup.select('.makers li'))
        json_data.extend(devices)

    return JsonResponse(json_data, safe=False)


async def getDevice(device):
    """Scrape a page of a particular device"""

    url = f'/{device}.php'
    html = await getDataFromUrl(url)
    print(html[:500])
    soup = BeautifulSoup(html, 'html.parser')

    display_size = soup.find('span', {'data-spec': 'displaysize-hl'}).text
    display_res = soup.find('div', {'data-spec': 'displayres-hl'}).text
    camera_pixels = soup.find('span', {'data-spec': 'camerapixels-hl'}).text
    video_pixels = soup.find('div', {'data-spec': 'videopixels-hl'}).text
    ram_size = soup.find('span', {'data-spec': 'ramsize-hl'}).text
    chipset = soup.find('div', {'data-spec': 'chipset-hl'}).text
    battery_size = soup.find('span', {'data-spec': 'batsize-hl'}).text
    battery_type = soup.find('div', {'data-spec': 'battype-hl'}).text
    popularity_percentage = soup.find('li', class_='light pattern help help-popularity').find('strong').get_text(strip=True)
    popularity = float(popularity_percentage.rstrip("%"))

    quick_spec = [
        {'name': 'Display size', 'value': display_size},
        {'name': 'Display resolution', 'value': display_res},
        {'name': 'Camera pixels', 'value': camera_pixels},
        {'name': 'Video pixels', 'value': video_pixels},
        {'name': 'RAM size', 'value': ram_size},
        {'name': 'Chipset', 'value': chipset},
        {'name': 'Battery size', 'value': battery_size},
        {'name': 'Battery type', 'value': battery_type},
        {'name': 'Popularity', 'value': popularity}
    ]

    name = soup.find('h1', {'class': 'specs-phone-name-title'}).text
    img = soup.find('div', {'class': 'specs-photo-main'}).find('img').get('src')

    detail_spec = []
    spec_nodes = soup.find_all('table', class_='pricing')

    pricing = []
    for spec_node in spec_nodes:
        spec_list = []
        category = spec_node.find('th')
        if category is not None:
            category = category.text
            spec_items = spec_node.find_all('tr')

            for spec_item in spec_items:
                spec_list.append({
                    'name': spec_item.find('td', {'class': 'ttl'}).text,
                    'value': spec_item.find('td', {'class': 'nfo'}).text,
                })

            if category:
                detail_spec.append({
                    'category': category,
                    'specifications': spec_list,
                })
        else:
            # Reached pricing section
            variants = spec_node.find_all('tr')

            for variant in variants:
                price = [
                    {'variant': variant.find('td').text},
                    {'price': variant.find('a').text},
                    {'site_img_url': variant.find('img')['src']},
                ]
                pricing.append(price)

    return {
        'name': name,
        'img': img,
        'quick_spec': quick_spec,
        'detail_spec': detail_spec,
        'pricing': pricing
    }
