URL Shortener is a Django App that stores and returns shortened versions of URLs and it redirects to the original
URL when requested, tracking the number of visits if desired.

It can be launched with Docker and these are the steps to get it up and running:
$ docker-compose build
$ docker-compose run us us-ctl migrate
$ docker-compose run us us-ctl createsuperuser
$ docker-compose up

To run the tests:
$ docker-compose run us us-ctl test

The application consists in three parts:
- <your_domain>/admin: standard django admin site.
- <your_domain>/<short_code>/: view that takes a short url and redirects to the original.
- <your_domain>/shorten_url/: single endpoint to create a shortened url.

USAGE:

    Request:
        POST <your_domain>/shorten_url/
        body:
        {
            "url": "www.google.com"
        }

    Response:
        Status code: 201
        {
            "url": "http://www.google.com",
            "shortened_url": "<your_domain>/cgwONASs"
        }

    GET <your_domain>/cgwONASs redirects to "http://www.google.com"


Some decisions taken:
- I decided to use Django because it allows me to create a web app with an admin site just out of the box and it has
  some libraries I knew would be very useful in this case like djangorestframework to build the API and django-redis.
- I first used URLField in the serializer but this kind of field doesn't consider as valid any urls that don't
  include the protocol, same with URLValidator. Even though this is more accurate, I decided to make the tool a bit
  more flexible and allow urls without protocol after all, so I had to implement my own validation, to add the protocol
  if missing and then use Django URLValidator.
- I added an extra feature to track the number of visits, that was not required, because I think it'd very useful and
  most of the similar tools include it. This could cause some delays in the request though, so I decided to do this
  update asynchronously, using Celery. If not desired, this feature can be turned off with a setting called TRACK_VISITS.
- Finally, I used redis to store the entries in cache, so we don't need to access the database for every GET request.
  This is very important in case the number of requests is very high. By default, I set the number of cache entries to
  1000 and the timeout to 1 day but these values are also configurable in settings and they could be set to higher
  numbers, even allowing cache entries to never expire automatically.

About scaling:
The webservice could be deployed in several nodes, all connected to the same database directly (or using a master/slave
configuration) to be able to handle more requests in parallel. The redis cache can be set to store more entries and have
a longer expiration time (so it's more likely that the entries are in the cache and the requests can be answered more
quickly). In case of a short_code not being in the cache, the url and short_code fields are also indexed to make the
queries to the database slightly faster.
