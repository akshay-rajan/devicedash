# DeviceDash

![home](tech/devicedash/static/screenshots/home.png)

 _A Smartphone Recommendation Website using Django._

In a world brimming with a multitude of smartphone options, making the right choice can often feel like navigating a labyrinth. That's where **DeviceDash** comes in.
Finding a smartphone that seamlessly integrates into your lifestyle, meets your requirements, and fits your budget is of great importance. DeviceDash simplify the steps one needs to take by recommending the most suitable smartphone within a few seconds. This user-friendly, responsive website lets the user choose a price range, with just a few clicks, and returns the top 10 most apt smartphones in that range. The simplicity and efficiency of this project empowers people overwhelmed by the myriad options available, offering a straightforward solution to finding their perfect match.


 
 ## Design

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
   * Search - Done
   * Design - Done



   
 3. Display phones according to user input

 ## Implementation



### scrape.py
* getDataFromUrl(url) - returns the source of a page
* getBrands() - returns a list of all brands
* getBrand(brand_id) - returns a list of all phones of a particular brand
* getNextPage(beautifulsoup_object) - returns the next page, if there is one
* getDevice(device_id) - returns all details regarding a device

* getDevices(soup, devices_list) - returns a refined list of devices, to use in the website