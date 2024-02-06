# DeviceDash
 A Smartphone Recommendation Website made with Django.

 ## Requirements

1. Let user enter a price interval and display the top 10 smartphones on that price.

2. When a phone is selected, display its features in detail.

3. Enable users to add a phone to cart.

 ## Design

 1. Analyze how to recommend the phones
    The website recommends the phones based on their popularity. Hence, we need to store that too.
    - Scrape popularity percentage --- Done


 2. Move all data to the database
    1. Get the list of brands
    2. For each brand, get the list of phones
    3. For each phone, store all its details

    Database Design:
      1. Brands
         |column|datatype|constraints|
         |------|--------|-----------|
         |brand_id|int|Primary Key|
         |brand|string||
      2. Phones
         |column|datatype|constraints|
         |------|--------|-----------|
         |brand|Brands|Foreign Key|
         |device_id|int|Primary Key|
         |name|string||
      3. Specifications
         |column|datatype|constraints|
         |------|--------|-----------|
         |device|Phones|Foreign Key|
         |img|url||
         |quick_spec|json||
         |pricing|json||
         |popularity|float||
       

   * Create Models - Done
   * Fetching - Done
   * Storing Brands - Done
   * Storing Phones - Done
   * Storing Specs - Done
   * Fetching Database === Fail
      New Table to create
   * Create "Devices" - Done

      |column|datatype|
      |------|--------|
      |brand|f-key|
      |device|f-key|
      |price|int|
      |popularity|float|
   * Storing in Devices - Done (currency conversion)
   * Find Phone - Done
   * View Phone - Done
   * Home - Done 
   * Login - Done
   * Logout - Done
   * Add Phone - Done
   * All Phones - Done (Pagination)
   * Search - todo



   
 3. Display phones according to user input

 ## Implementation

### scrape.py
* getDataFromUrl(url) - returns the source of a page
* getBrands() - returns a list of all brands
* getBrand(brand_id) - returns a list of all phones of a particular brand
* getNextPage(beautifulsoup_object) - returns the next page, if there is one
* getDevice(device_id) - returns all details regarding a device

* getDevices(soup, devices_list) - returns a refined list of devices, to use in the website