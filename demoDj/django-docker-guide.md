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

### Install Docker Compose:
docker-compose to run multiple container configurations, f.i manage startup dependencies and specify startup order

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
mkdir demoDj && cd demoDj

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
## Step 4: Create Dockerfile
## Step 5: Create docker-compose.yml
## Step 6: Create .dockerignore
## Step 7: Create .env file
- AELZ_01: remove .env as potentially unsecure, use dynamical binding instead 

## Step 8: Update Django settings.py

- AELZ_02: correct unnecesary settings later

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

- AELZ_03 for steps above see corresponding files in repo
- AELZ_04 create dbuser in advance, f.i. in entrypoint.sh or as python script from host, if simpler ?
- Add entrypoint.šh instead of cmd ? 

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

curl -X POST http://localhost:8000/api/ \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Access Django admin
# Navigate to: http://localhost:8000/admin/

- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **API Docs (Swagger)**: http://localhost:8000/api/docs/
- **API Docs (ReDoc)**: http://localhost:8000/api/redoc/

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

psql  -U djangouser djangodb
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

6. ** Running server **
## manage.py == django-admin (cli)
python3 manage.py runserver

Geting objects from model
--------------------------
Notification.objects.all()
Notification.objects.all().values()
Notification.objects.all().count()
Notification.objects.filter(
                    origin=alarm_1['origin'],
                    notification_id = alarm_1['notification_id'],
                    time_cleared = alarm_1['time_cleared']).count()

- serialize    - >  to network
- desereialize  ->  from network to model

- boilerplate html  Set of predefined html templates for Djnago web development.
- http://www.initializr.com/  basic html  boilerplates


Django templates
----------------
https://djangocentral.com/static-assets-in-django/


Django CLI
----------

python3 manage.py shell
from notification_inventory.models import Notification
qs=Notification.objects.all()
qs.get().additional_text
qs.get().notification_id
qs.values()


## Next Steps

Your Django REST Framework application is now fully Dockerized and ready for development and deployment!
```
