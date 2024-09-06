FROM python:3.9

# Install dependencies and wait-for-it
RUN apt-get update && apt-get install -y netcat
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Set working directory and copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install Flask SQLAlchemy Flask-SQLAlchemy psycopg2

# Use wait-for-it to delay start until DB is ready
CMD ["wait-for-it.sh", "db:5432", "--", "python", "take_home.py"]
