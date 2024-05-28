ARG REQUIREMENTS_FILE

FROM python:3.12

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN set -x && \
	apt-get update && \
	apt -f install	&& \
	apt-get -qy install netcat-traditional && \
    apt install -y build-essential libpoppler-cpp-dev pkg-config python3-dev && \
	rm -rf /var/lib/apt/lists/* 


# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000


# RUN pip install pip==23.1.2 && \
# RUN pip install setuptools==65.5.0 && \
RUN pip install -r requirements.txt

# CMD ["sh", "/entrypoint-web.sh"]
# CMD python manage.py runserver 0.0.0.0:8000
