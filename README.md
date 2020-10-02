# SBTools
SBTools is a Django web service for browsing the SponsorBlock database (https://sponsor.ajay.app/).  
The project is tested to work on Python 3.8.

There is a publicly hosted instance of this service at https://sb.ltn.fi/

## Installation & Usage

### Development
For development you can clone the repo, install requirements.txt (in a venv preferably) and run the Django development server with `(venv) python manage.py runserver`.

Database should still be migrated to PostgreSQL (eg. `pgloader database.db postgresql://sponsorblock@localhost/sponsorblock`) and modified with `INSERT INTO config VALUES ('updated', now());` or similar.  
Database connection details are configured in SBtools/settings/development.py  
The SECRET_KEY doesn't need changing necessarily.

### Production
There are helpful files under docs/ for deploying the service.

All examples assume a Linux user `sponsorblock` with home folder at `/srv/sponsorblock/`
and proxying the site through Nginx with webroot at `/srv/http/sbtools/`

You should also have a PostgreSQL user `sponsorblock` with a database called `sponsorblock`.  
Based on brief testing, using the SQLite database has abysmal performance.

Installing before running could look like the following

```bash
[sponsorblock]$ git clone https://github.com/Lartza/SBtools.git
[sponsorblock]$ python -m venv /srv/sponsorblock/SBtools/venv
[sponsorblock]$ /srv/sponsorblock/SBtools/venv/bin/pip install -r /srv/sponsorblock/SBtools/requirements.txt
[sponsorblock]$ /srv/sponsorblock/SBtools/venv/bin/pip install gunicorn
[sponsorblock]$ DB_PASSWORD='changeme' SECRET_KEY='changeme' 'STATIC_ROOT=/srv/http/sbtools/static/' DJANGO_SETTINGS_MODULE='SBtools.settings.production' /srv/sponsorblock/SBtools/venv/bin/python /srv/sponsorblock/SBtools/manage.py collectstatic --noinput
```

The DB_PASSWORD, SECRET_KEY and STATIC_ROOT variables are also present in files under docs/ and should be modified as needed.  
SECRET_KEY should be a large random value and kept secret. You could generate one on https://djecrety.ir/

After installation the files under docs/ should help with migrating the database to PostgreSQL and running the service.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)