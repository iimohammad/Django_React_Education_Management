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
