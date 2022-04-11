-- Creation of product table
CREATE TABLE IF NOT EXISTS city_temperature (
  dt DATE NOT NULL,
  temperature FLOAT,
  uncertainty FLOAT,
  city TEXT NOT NULL,
  country TEXT,
  latitude TEXT NOT NULL,
  longitude TEXT NOT NULL,
  PRIMARY KEY (city, dt, latitude, longitude)
);

COPY city_temperature(dt, temperature, uncertainty, city, country, latitude, longitude)
FROM '/GlobalLandTemperaturesByCity.csv'
DELIMITER ','
CSV HEADER;
