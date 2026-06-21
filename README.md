# holbertonschool-hbnb
A web application allowing users to list places to rent to other users, built using Python and Flask.
# Installation and Running
## Pre-requisites:
- An installation of [Python3](https://www.python.org/downloads/).
## Setup
Download this repository by either:
- Running `git clone https://github.com/SiSiSierra/holbertonschool-hbnb.git` in a terminal at the location you want the folder.
- Clicking "Code" at the top of this page and click "Download zip" in the box that appears. Extract the contents together to a folder.

Download the remaining dependencies by running `pip install -r requirements.txt` in a terminal at the folder you created in the previous step.
## Running
Begin the app by running `python run.py` in a terminal in the project folder. You should see something like
```
* Serving Flask app 'app'
...
* Running on http://127.0.0.1:5000
Press CTRL+C to to quit
```
From the machine running the app, the API can be accessed from [localhost:5000/api/v1/](http://localhost:5000/api/v1/)
# API
The documentation listed below can also be accessed and interacted with by running the app and accessing [localhost:5000/api/v1/](http://localhost:5000/api/v1/)
* `/users`
  - GET: All users and user data
  - POST: A new user
  * `/users/{id}`
    - GET: Specific user by id
    - PUT: update attributes for specific user

* `/amenities`
  - GET: All amenities and amenity data
  - POST: A new amenity
  * `/amenities/{id}`
    - GET: Specific amenity by id
    - PUT: update attributes for specific amenity

* `/places`
  - GET: All places and place data
  - POST: A new place
  * `/places/{id}`
    - GET: Specific place by id
    - PUT: update attributes for specific place
    * `/places/{id}/reviews`
      - GET: All reviews for a specific place

* `/reviews`
  - GET: All reviews and review data
  - POST: A new review
  * `/places/{id}`
    - GET: Specific review by id
    - PUT: update attributes for specific review
    - DELETE: a specific review by id
