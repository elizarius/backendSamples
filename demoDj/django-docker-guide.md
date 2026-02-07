# Dockerizing Django REST Framework Application from Scratch on Linux

## Prerequisites
- Linux system (Ubuntu/Debian/CentOS/etc.)
- Docker installed
- Docker Compose installed (optional but recommended)

## Project Structure
```
demoDj/
├── app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── .env
```

## Step 1: Install Docker on Linux

### For Ubuntu/Debian:
```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Log out and back in, then verify
docker --version
```

### For CentOS/RHEL:
```bash
# Install required packages
sudo yum install -y yum-utils

# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install docker-ce docker-ce-cli containerd.io

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### Install Docker Compose:
```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

## Step 2: Create Django Project (if starting fresh)

```bash
# Create project directory
mkdir myproject && cd myproject

# Create virtual environment (optional, for development)
python3 -m venv venv
source venv/bin/activate

# Install Django and DRF
pip3 install django djangorestframework psycopg2-binary gunicorn python-decouple
# pip3 install Django --upgrade if necessary 

# Create Django project
django-admin startproject app .


# Create an API app
python manage.py startapp api

# Generate requirements.txt
pip freeze > requirements.txt
```

## Step 3: Create requirements.txt

```txt
Django>=4.2,<5.0
djangorestframework>=3.14.0
psycopg2-binary>=2.9.9
gunicorn>=21.2.0
python-decouple>=3.8
whitenoise>=6.6.0
django-cors-headers>=4.3.0
```
## Step 4: Create Dockerfile

```dockerfile
# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create static files directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
```

## Step 5: Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=djangodb
      - POSTGRES_USER=djangouser
      - POSTGRES_PASSWORD=djangopass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U djangouser"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: sh -c "python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key-here-change-in-production
      - DATABASE_URL=postgresql://djangouser:djangopass@db:5432/djangodb
      - ALLOWED_HOSTS=localhost,127.0.0.1
    depends_on:
      db:
        condition: service_healthy

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

## Step 6: Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.gitignore
.mypy_cache
.pytest_cache
.hypothesis
*.db
*.sqlite3
db.sqlite3
media/
.env
.venv
*.swp
*.swo
*~
.DS_Store
node_modules/
```

## Step 7: Create .env file

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-generate-a-new-one
DATABASE_URL=postgresql://djangouser:djangopass@db:5432/djangodb
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
POSTGRES_DB=djangodb
POSTGRES_USER=djangouser
POSTGRES_PASSWORD=djangopass
```

## Step 8: Update Django settings.py

```python
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-changeme')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',  # Your API app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='djangodb'),
        'USER': config('POSTGRES_USER', default='djangouser'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='djangopass'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## Step 9: Create nginx.conf (Optional, for production)

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## Step 10: Build and Run

### Using Docker Compose (Recommended):

```bash
# Build the images
docker-compose build

# Start the services
docker-compose up -d

# View logs
docker-compose logs -f

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v
```


### Using Docker only:

```bash
# Build the image
docker build -t django-drf-app .

# Run PostgreSQL container
docker run -d \
  --name postgres-db \
  -e POSTGRES_DB=djangodb \
  -e POSTGRES_USER=djangouser \
  -e POSTGRES_PASSWORD=djangopass \
  -p 5432:5432 \
  postgres:15

# Run Django container
docker run -d \
  --name django-app \
  --link postgres-db:db \
  -e DATABASE_URL=postgresql://djangouser:djangopass@db:5432/djangodb \
  -p 8000:8000 \
  django-drf-app

# View logs
docker logs -f django-app
```

## Step 11: Useful Docker Commands

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# View images
docker images

# Remove an image
docker rmi <image_id>

# Execute command in running container
docker exec -it <container_id> bash

# View container logs
docker logs <container_id>

# With docker-compose:
docker-compose ps
docker-compose logs -f web
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Step 12: Testing the Application

```bash
# Check if containers are running
docker-compose ps

# Test the API
curl http://localhost:8000/api/

# Access Django admin
# Navigate to: http://localhost:8000/admin/

# Run tests
docker-compose exec web python manage.py test
```

## Troubleshooting

### Container won't start:
```bash
# Check logs
docker-compose logs web

# Check database connection
docker-compose exec web python manage.py dbshell
```

### Permission issues:
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Database connection issues:
```bash
# Ensure database is ready
docker-compose exec db pg_isready -U djangouser

# Check environment variables
docker-compose exec web env | grep DATABASE
```

### Port already in use:
```bash
# Find process using port 8000
sudo lsof -i :8000

# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

## Production Considerations

1. **Security:**
   - Generate strong SECRET_KEY
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS properly
   - Use environment variables for sensitive data
   - Enable HTTPS/SSL

2. **Performance:**
   - Use production-grade WSGI server (gunicorn)
   - Configure worker processes appropriately
   - Use Redis for caching
   - Set up CDN for static files

3. **Database:**
   - Regular backups
   - Use managed database service
   - Configure connection pooling

4. **Monitoring:**
   - Set up logging
   - Use monitoring tools (Sentry, New Relic)
   - Configure health checks

5. **Scaling:**
   - Use container orchestration (Kubernetes, Docker Swarm)
   - Load balancing
   - Horizontal scaling

## Next Steps

1. Add CI/CD pipeline (GitHub Actions, GitLab CI)
2. Implement Redis for caching and Celery for async tasks
3. Set up proper logging and monitoring
4. Configure automated backups
5. Implement proper security measures
6. Add API documentation (Swagger/ReDoc)
7. Set up staging and production environments

Your Django REST Framework application is now fully Dockerized and ready for development and deployment!
```
