# SI507_final_project

HuangyiLi

[Link to this repository](https://github.com/Lhuangyi/SI507_final_project)

---

## Project Description

In my project, I have done the following things:
- Write code to scrape data in coursera(https://www.coursera.org/about/partners/us). I scraped about 180 universities to collect university information including university name, courses list and instructors list.
- Store scraped data in a json file and then define an up_load_data function to write data into database.
- Write code to integrate scraped data with a Flask application
- Integrate models with the Flask framework to build a Flask app
- Write code to show the data and design front-end web page

## How to run

1. First, you should install all requirements with `pip install -r requirements.txt`)
3. Second, you should run `python SI507project_tools.py` to scrape data form website. 
    (Since the website is keep updating, there may be some urls which are able to scraped. I will try my best to keep tracking those changes! If you run the code and find that there is a error writen "NoneTpye", please instert the following lines to line 110:
    `elif url == "bad_url":`
    `continue`
    bad_url is the url showed in the bash console that can't be scraped.
    
3. Third, when finished Scraping data, you should run `python SI507project_tests.py ` to test.
4. Then, you should run `python SI507project_app.py runserver` and copy the address: (http://127.0.0.1:5000/)
 
## How to use

1. In this flask app users can show scraped in a web page.
2. Users can also check and delete exited courses,universities and instructors.
3. Screenshot:
    homepage: Users can click the button:"home" in navigation bar to access homepage
    ![alt text](https://github.com/Lhuangyi/SI507_final_project/blob/master/img/E1C6A408804C892BC00586894047C402.png)
    
    add page: Users can click the button:"Add University" in navigation bar to access create page
    ![alt text](https://github.com/Lhuangyi/SI507_final_project/blob/master/img/3F3F0FE5C4FCE2D49A12D81F6D3313D9.png)
    detail page: Users can click the name of unversity to enter detail page and click "delete" to remove corresponding items.
    ![alt text](https://github.com/Lhuangyi/SI507_final_project/blob/master/img/864B9EC8C14D29A431FFE504E082CAE6.png)
4. I am still working on login function, I will keep updating this project and acquiring flask knowledge.

## Routes in this application
- `/` -> this is the home page
- `/login` -> this route has a form for user input to login( still work on it)
- `/add'->` this route has a form for user input to create a new university
- `/university?id=<university_id>` -> this route to enter spectific university detail page
- `/delete_university/<university_id>` -> this route can delete a specific university
- `/delete_instructor/<instructor_id>` -> this route can delete a specific instructor
- `/delete_universiy/<university_id>` -> this route can delete a specific university

## How to run tests
You should run `python SI507project_tests.py `to test SI507project_tools.py


## In this repository:
- [img]
- [database]
  - database.001.jpeg
- [static]
  - [img]
    - logo.jpg
  - style.css
- [templates]
  - add.html
  - addcourse.html
  - addinstructor.html
  - base.html
  - detail.html
  - index.html
  - login.html
  - success.html
- SI507project_tools.py
- SI507project_tests.py
- SI507project_app.py
- database.pdf
- requirements.txt

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [x] Use of a new module
- [ ] Use of a second new module
- [x] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [x] At least one form in your Flask application
- [x] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [x] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
