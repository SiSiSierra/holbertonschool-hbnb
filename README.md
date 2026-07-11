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

In a terminal, type `flask shell` and then `db.create_all()` to create the database. If you don't do this, nothing sent to the app will be saved.

## Running
Everytime the app is run, a default admin user to created from a template in `run.py`.

IT IS EXTREMELY RECOMMENDED TO CHANGE THE EMAIL AND PASSWORD FIELDS IN `run.py` BEFORE RUNNING THE APP FOR THE FIRST TIME

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
* `/auth/login`
  - POST: A pre-existing user's email and password to get a login token. This token must be included in the headers for any request that regards modifying data, in the form `Authorization: Bearer <token>`.

* `/users`
  - GET: All users and user data
  - POST: A new user (admin only)
  * `/users/{id}`
    - GET: Specific user by id
    - PUT: update attributes for specific user (admin only)

* `/amenities`
  - GET: All amenities and amenity data
  - POST: A new amenity (admin only)
  * `/amenities/{id}`
    - GET: Specific amenity by id
    - PUT: update attributes for specific amenity (admin only)

* `/places`
  - GET: All places and place data
  - POST: A new place (requires login token)
  * `/places/{id}`
    - GET: Specific place by id
    - PUT: update attributes for specific place (requires login token from place's owner or admin)
    * `/places/{id}/reviews`
      - GET: All reviews for a specific place

* `/reviews`
  - GET: All reviews and review data
  - POST: A new review (requires login token)
  * `/places/{id}`
    - GET: Specific review by id
    - PUT: update attributes for specific review (requires login token from review's owner or admin)
    - DELETE: a specific review by id (requires login token from review's owner or admin)
