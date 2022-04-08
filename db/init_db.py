import csv
from sqlalchemy import create_engine
import os


USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')

db_string = f"postgres://{USER}:{PASSWORD}@127.0.0.1:5432/{DB}"

db = create_engine(db_string)

print("Hello")

with open('GlobalLandTemperaturesByCity.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        date = row[0]
        temp = float(row[1])
        unc = float(row[2])
        city = row[3]
        country = row[4]

        db.execute(f"""
            INSERT INTO city_temperature
            (dt, temperature, uncertainty, city, country)
            VALUES ({date}, {temp}, {unc}, '{city}', '{country}')
            """)
        break