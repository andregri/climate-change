FROM postgres:14
ENV POSTGRES_USER="andrea"
ENV POSTGRES_PASSWORD="password"
ENV POSTGRES_DB="climate_db"
COPY GlobalLandTemperaturesByCity.csv .
COPY schema.sql /docker-entrypoint-initdb.d/create_tables.sql