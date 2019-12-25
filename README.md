# django-rest-telenor

##clone
`git clone https://github.com/ishmam-hossain/django-rest-telenor.git`

###single command run
> `python manage.py runapi`


This command will install all the dependencies and run the the server at `Port` `8000`.
<br>
> `Django` needs to be installed beforehand as the command is handled by `Django` itself.

###dependencies
`Redis` has been used as database. Before running the server a `.env` file is suggested to be added with the
`keys` as given with appropriate values:
> `REDIS_HOST=`<br>
> `REDIS_PORT=`<br>

if `.env` file is not found then by default the app will connect to `localhost` at `port` `6379`.


###packages used
`pipenv`, `python-decouple`, `redis`, `django`, `django_rest_framework`