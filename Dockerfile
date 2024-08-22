# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy the system requirements file
COPY apt-requirements.txt .

# Install system dependencies
RUN apt-get update && xargs apt-get install -y < apt-requirements.txt && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/gbdev/rgbds/releases/download/v0.7.0/rgbds-0.7.0-linux-x86_64.tar.xz \
    && mkdir rgbds \
    && tar xf rgbds-0.7.0-linux-x86_64.tar.xz -C rgbds \
    && cd rgbds \
    && ./install.sh \
    && rm ../rgbds-0.7.0-linux-x86_64.tar.xz  # Clean up the tar file

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug

# RUN python manage.py collectstatic --noinput

ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=admin@example.com \
    DJANGO_SUPERUSER_PASSWORD=adminpassword

RUN python manage.py migrate --noinput && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
    User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"

RUN python manage.py makemigrations --noinput

RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.get_or_create(username='anonymous', defaults={'email': 'anonymous@example.com'})"

RUN python manage.py shell -c "from patches.views import add_data_to_bd; add_data_to_bd()"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi", "-k", "gevent", "--worker-connections", "1000"]