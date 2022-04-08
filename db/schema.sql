-- Creation of product table
CREATE TABLE IF NOT EXISTS city_temperature (
  id SERIAL,
  dt DATE,
  temperature FLOAT,
  uncertainty FLOAT,
  city TEXT,
  country TEXT,
  latitude TEXT,
  longitude TEXT,
  PRIMARY KEY (id)
);

COPY city_temperature(dt, temperature, uncertainty, city, country, latitude, longitude)
FROM '/GlobalLandTemperaturesByCity.csv'
DELIMITER ','
CSV HEADER;
