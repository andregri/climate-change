FROM postgres:14
ENV POSTGRES_USER="andrea"
ENV POSTGRES_PASSWORD="password"
ENV POSTGRES_DB="climate_db"
COPY GlobalLandTemperaturesByCity.csv .
RUN apt-get update -y && apt-get install -y libpq-dev gcc python3 python3-dev python3-pip
RUN python3 --version
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY schema.sql /docker-entrypoint-initdb.d/create_tables.sql
COPY init_db.py .
