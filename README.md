# django-rest-telenor

## clone
> `git clone https://github.com/ishmam-hossain/django-rest-telenor.git`

### single command run
> `python manage.py runapi`


This command will install all the dependencies and run the the server at `Port` `8000`.
<br>

        pip install -r requirements.txt
        redis-server
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver
        
> `Django` needs to be installed beforehand as the command is handled by `Django` itself.
> And `pipenv` is suggested for package installation. 

### dependencies
`Redis` has been used as database. Before running the server a `.env` file is suggested to be added with the
`keys` as given with appropriate values:
> `REDIS_HOST=`<br>
> `REDIS_PORT=`<br>

if `.env` file is not found then by default the app will connect to `localhost` at `port` `6379`.

### API
All routes must be prefixed with `/api`
>   `localhost:8000/api/values`

###### GET /values
Returns all the key-values in dictionary form in the key `data` along with other information & `resets ttl` for all keys.
```json
{
  "status": "success",
  "total": 3,
  "data": {
    "key1": "test1",
    "key2": "test2",
    "key3": "test3"
  },
  "not_found": []
}
```

###### GET /values?keys=key1,key2,key3,key4,key5
Returns all the key-values asked for in dictionary form in the key `data` along with other information & `resets ttl` for all the asked keys.
```json
{
  "status": "success",
  "total": 3,
  "data": {
    "key1": "test1",
    "key2": "test2",
    "key3": "test3"
  },
  "not_found": [
    "key4",
    "key5"
  ]
}
```
* `not_found` list contains the keys asked for which do not exist in the database or have expired.

###### POST /values
Stores values passed in the `json` body & `sets ttl`.
```json
{
  "status": "success",
  "message": "successfully inserted 3 keys.",
  "errors": []
}
```
If some error occurs for any key value pair then the response will be like-
```json
{
  "status": "success",
  "message": "successfully inserted 3 keys.",
  "errors": [
      "key4 -> some error" 
   ]
}
```
* Other key value will be stored as usual.

###### PATCH /values
Updated the key-value pairs in the `json` & `resets ttl`. 
```json
{
  "status": "success",
  "message": "successfully updated 3 keys.",
  "not_found": [
    "key4",
    "key5"
  ],
  "errors": []
}
```

### packages used
`pipenv`, `python-decouple`, `redis`, `django`, `django_rest_framework`
