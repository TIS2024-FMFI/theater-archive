# theater-archive
Archive for theater

Tento repozitár obsahuje školský projekt pre predmet Tvorba informačných systémov 2024/2025. Téma bola tvorba informačného systému pre národné divadlo SND, pre spávu informácií v archíve. Systém je určný pre zamestnancov archívu SND, ako aj pre širokú verejnosť. Projekt bol vytvorený ako webová Django aplikácia, ktorá okrem hlavného jazyka Python využíva aj javascript a html.

## Setup Environment

### Prerequisites

- PostgreSQL 17.2
- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)


### Create database
REATE DATABASE theater_archive;
CREATE USER 'user_for_comunication_with_db' WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE theater_archive TO user_for_comunication_with_db;


### Clone the Repository

```bash
git clone https://github.com/TIS2024-FMFI/theater-archive.git
cd theater-archive

# Create virtual environment
python -m venv venv

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Activate virtual environment (Windows)
venv\Scripts\activate


pip install -r requirements.txt

# edit django_vyvojove_prostredie/mysite/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'theater_archive',
        'USER': '{user_for_comunication_with_db}',
        'PASSWORD': '{password}',
        'HOST': 'localhost',
        'PORT': '{port_that_db_runs_on}',
    }
}

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1", "localhost", {list of allowed hosts separated by comma}]


# Apply database migrations
python manage.py migrate

# Create a superuser (follow the prompts to set up a superuser account)
python manage.py createsuperuser

python manage.py collectstatic

python3 manage.py runserver 0.0.0.0:8000
```
