FROM postgres:14
ENV POSTGRES_USER="andrea"
ENV POSTGRES_PASSWORD="password"
ENV POSTGRES_DB="climate_db"
COPY schema.sql /docker-entrypoint-initdb.d/create_tables.sql
COPY GlobalLandTemperaturesByCity.csv .
COPY requirements.txt .
RUN apt-get update -y && apt-get install -y python3 python3-dev python3-pip
RUN python3 --version
RUN pip install -r requirements.txt
COPY init_db.py .
RUN python3 init_db.py
