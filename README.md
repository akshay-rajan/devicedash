# DeviceDash
 A Smartphone Recommendation Website made with Django.

 ## Requirements

1. Let user enter a price interval and display the top 10 smartphones on that price.

2. When a phone is selected, display its features in detail.

3. Enable users to add a phone to cart.

 ## Design

 1. Analyze how to recommend the phones
    The website recommends the phones based on their popularity. Hence, we need to store that too.
    Todo: Scrape popularity percentage
 2. Move all data to the database
 3. Display phones according to user input

 ## Implementation

### scrape.py
* getDataFromUrl(url) - returns the source of a page
* getBrands() - returns a Json list of all brands
* getBrand(brand_id) - returns a list of all phones of a particular brand
* getNextPage(beautifulsoup_object) - returns the next page, if there is one
* getDevice(device_id) - returns all details regarding a device

* getDevices(soup, devices_list) - returns a refined list of devices, to use in the website