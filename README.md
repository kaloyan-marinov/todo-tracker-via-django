```
$ cp .env.template .env

# Edit the content of `.env` as per the comments/instructions therein.
```

the remainder of this description will explain how to
use Docker to serve the persistence layer,
but use `localhost` (= the local network interface) to serve the Django application

---

```
$ python3 --version
Python 3.8.3

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

```
docker run \
    --name container-t-t-v-d-postgres \
    --mount source=volume-t-t-v-d-postgres,destination=/var/lib/postgresql/data \
    --env-file .env \
    --publish 5432:5432 \
    postgres:15.1
```

(

OPTIONALLY, verify that the previous step did start serving a PostgreSQL server:

```
$ docker container exec -it container-t-t-v-d-postgres /bin/bash

root@<container-id> psql \
    --host=localhost \
    --port=5432 \
    --username=<the-value-for-POSTGRES_USER-in-the-.env-file> \
    --password \
    <the-value-for-POSTGRES_DB-in-the-.env-file>

<the-value-for-POSTGRES_DB-in-the-.env-file>=# \d
Did not find any relations.
```

)

```
(venv) $ python manage.py migrate
```

---

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```

```
# Issue requests to the application by
# either (a) using your web browser to navigate to http://localhost:8000/api/ ,
# or (b) launching a second terminal instance and executing the following command:

$ http localhost:8000/api/

HTTP/1.1 200 OK
Allow: OPTIONS, GET
Content-Length: 154
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Mon, 09 Jan 2023 06:03:50 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "Create": "/task-create/",
    "Delete": "/task-delete/<str:pk>/",
    "Detail View": "/task-detail/<str:pk>/",
    "List": "/task-list/",
    "Update": "/task-update/<str:pk>/"
}
```

```
Issue the following additional requests to the application:

$ http POST localhost:8000/api/task-create/
HTTP/1.1 400 Bad Request
Allow: POST, OPTIONS
Content-Length: 49
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 10 Jan 2023 05:36:26 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "error": "the submitted 'Task data' was invalid"
}

$ http POST localhost:8000/api/task-create/ \
    title='get salad'
HTTP/1.1 201 Created
Allow: POST, OPTIONS
Content-Length: 46
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 10 Jan 2023 05:49:26 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "completed": false,
    "id": 1,
    "title": "get salad"
}

$ http POST localhost:8000/api/task-create/ \
    title='do laundry' \
    completed='True'
HTTP/1.1 201 Created
Allow: POST, OPTIONS
Content-Length: 46
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 10 Jan 2023 05:49:53 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "completed": true,
    "id": 2,
    "title": "do laundry"
}

$ http localhost:8000/api/task-list/
HTTP/1.1 200 OK
Allow: OPTIONS, GET
Content-Length: 95
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 10 Jan 2023 05:52:52 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "completed": false,
        "id": 1,
        "title": "get salad"
    },
    {
        "completed": true,
        "id": 2,
        "title": "do laundry"
    }
]
```
