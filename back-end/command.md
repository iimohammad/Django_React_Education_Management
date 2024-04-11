# Here You Can Find All Command to Use This Project
config secret key for proejct
```bash
python manage.py shell
```

```bash
from django.core.management.utils import get_random_secret_key
```

```bash
print(get_random_secret_key())
```
```bash
docker-compose up --build -d
docker-compose logs

```

```bash
celery -A config beat -l info
```
```bash
celery -A config worker -l info
```
Use Both of them by this command
```bash
celery -A config worker -B -l info
```
```bash
    python3 manage.py runserver
```


```bash
    python3 manage.py test
```

```bash
    pip install -r requirements.txt
```