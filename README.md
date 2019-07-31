# nicenotes

A webapp for storing notes and then sharing them with other users.

## Development Setup

Install the requirements using [pip](https://pip.pypa.io/en/stable/):

```bash
$ pip install -r requirements.txt
```

Download and install [PostgreSQL](https://www.postgresql.org/download/)
and setup a new user `django` with password `test`.

After that, perform Django migrations:

```bash
$ python manage.py migrate
```

Finally, start the server:

```bash
$ python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the app.
