# DeviceDash

![home](tech/devicedash/static/screenshots/home.png)

 _A Smartphone Recommendation Website using Django._

In a world brimming with a multitude of smartphone options, making the right choice can often feel like navigating a labyrinth. That's where **DeviceDash** comes in.
Finding a smartphone that seamlessly integrates into your lifestyle, meets your requirements, and fits your budget is of great importance. DeviceDash simplify the steps one needs to take by recommending the most suitable smartphone within a few seconds. This user-friendly, responsive website lets the user choose a price range, with just a few clicks, and returns the top 10 most apt smartphones in that range. The simplicity and efficiency of this project empowers people overwhelmed by the myriad options available, offering a straightforward solution to finding their perfect match.


## Distinctiveness and Complexity

DeviceDash is a web application which provides smartphone recommendation based on the price range entered by the user. The website is made using various skills and knowledge obtained during this course, combining them together to develop a practical and handy application. The website starts with a form that recieves a price range from the user. The form entries are validated using JavaScript. After recieving the price input, the user is taken to a page which displays the recommended phones based on user input. A large amount of data regarding smartphones is required to provide this. The data was obtained using *Web Scraping* in python. The website _gsmarena_ was scraped using **BeautifulSoup** module in python, to obtain data regarding all smartphones in the market. The scraping process required months of effort and was obeying all website guidelines, and following the *robots.txt* file of the site. The data was fetched from the website and stored to the Django Database as several models. The cards are displayed in a user-friendly and attractive design using CSS styles.

The application provides an "All Phones" button in the navigation bar, which lets users see a list of all phones available in the database. The search bar lets users search for a phone by the name or brand, and displays the result by querying the database using **Q**. There is also a facility for admin login, which lets the administrator add new phones to the database through a form. Admin can also logout from their account through a link in the navbar. The navigation bar is dynamically modified based on the current state of the website. The entire website is stylishly designed to attract users.

Buttons are included in the home page to quickly select a price range rather than entering the starting and ending prices, which categorizes the price range into Budget, Mid Range and Flagship phones. The data scraped to be used has undergone various cleanups before they were of suitable format. The project is sufficiently distinct from an e-commerce website or a social media website and uses almost all of the skills covered in the course. It uses Django on the backend, with multiple models and JavaScript on the front end, including stylish designing using CSS. 
 
 ## Contents

* [layout.html](tech/devicedash/templates/devicedash/layout.html): Defines the layout for the application, containing links to all pages and the search bar.
* [index.html](tech/devicedash/templates/devicedash/index.html): Defines the home page containing a form that lets users select the price range.
* [find.html](tech/devicedash/templates/devicedash/find.html): Returns the result of the query by the user as cards, displaying only the top 10 phones.
* [views.html](tech/devicedash/templates/devicedash/views.html): Renders a page containing all details and specifications regarding the phone selected by the user.
* [admin.html](tech/devicedash/templates/devicedash/admin.html): Lets the app administrator login to the website.
* [add.html](tech/devicedash/templates/devicedash/add.html): Renders a form that lets admin add a new phone to the database.
* [logout.html](tech/devicedash/templates/devicedash/logout.html): Lets admin log out.
* [results.html](tech/devicedash/templates/devicedash/results.html): Renders a page displaying the results of search query
* [all.html](tech/devicedash/templates/devicedash/all.html): Displays a page with a list of all phones in the database.


### [views.py](tech/devicedash/views.py)

This file contains all the django views for the project. The file starts with `index` function which renders the home page. The `find` function receives the user input of price range and returns the top 10 phones falling inside the price range, ordered by descending order of their popularity. When clicked on a card containing details of a phone rendered by this function, the `viewPhone` function takes the user to a page which displays all the details regarding that phone.

`storeData` is an **asynchronous** function which fetches data from the scraped website using functions from the **scrape.py** file, and stores them to the database. `storeToDevices` is a similar function which connects the data in different models by unifying them under a model named _Devices_.

The function `admin` returns a page for administrator login, meanwhile `logout_view` facilitates logout. `add` validates admin login, while rendering the page for adding a new phone to the database. `save` function saves the new phone to the database. `all_phones` returns a **Paginated** list of all phones in the database. `search` takes the smartphone name or brand name entered by the user in the search bar and renders a page containing all the search results.


### [models.py](tech/devicedash/models.py)
### [urls.py](tech/devicedash/urls.py)
### [utils.py](tech/devicedash/utils.py)
### [scrape.py](tech/devicedash/scrape.py)

## How to Run

1. Move to the repository containing the application
2. Install the dependencies by running

         pip install bs4

2. Start the server by
      
         py manage.py runserver

3. Open the website by clicking on the url in the terminal.

