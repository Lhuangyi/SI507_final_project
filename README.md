# SI507_final_project

HuangyiLi

[Link to this repository](https://github.com/Lhuangyi/SI507_final_project)

---

## Project Description

In my project, I have done the following things:
- Write code to scrape data in coursera(https://www.coursera.org/about/partners/us). I scraped 55 universities collecting university name, courses list and instructors list.
- Write code to integrate data scraped with a Flask application
- Integrate models with the Flask framework to build a Flask app
- Write code to show the data and design front-end web page

## What I have done:
  - Write code to scrape data
  - Integrate models with the Flask framework to build a Flask app
  - Write code to show the data and design front-end web page

## What I have not done:
  - Write code to integrate scraped data with a Flask application
  

## How to run

1. First, you should install all requirements with `pip install -r requirements.txt`)
2. Second, you should run `python runserve.py runserver `

## How to use

1. A useful instruction goes here
2. A useful second step here
3. (Optional): Markdown syntax to include an screenshot/image: ![alt text](image.jpg)

## Routes in this application
- `/index` -> this is the home page
- `/login` -> this route has a form for user input to login
- `/register` -> this route has a form for user input to register
- `/logout` -> this route has a form for user input to logout
- `/create` -> this route has a form for user input to create a new course
- `/delete_instructor/<instructor_id>` -> this route can delete a specific instructor
- `/delete_universiy/<university_id>` -> this route can delete a specific university

## How to run tests
You should run `python SI507project_tests.py `to test SI507project_tools.py


## In this repository:
- [database]
  - database.001.jpeg
- [static]
  -[img]
    -logo.jpg
  -style.css
- [templates]
  -add.html
  -base.html
  -detail.html
  -index.html
  -login.html
  -register.html
  -user.html
-SI507project_tools.py
-SI507project_tests.py
-database.pdf
-runserver.py
-requirements.txt

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
- [x] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [x] At least one form in your Flask application
- [x] Templating in your Flask application
- [x] Inclusion of JavaScript files in the application
- [ ] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
