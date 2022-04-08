-- Creation of product table
CREATE TABLE IF NOT EXISTS city_temperature (
  id INT NOT NULL,
  dt DATE,
  temperature DOUBLE,
  uncertainty DOUBLE,
  city TEXT,
  country TEXT,
  latitude DOUBLE,
  longitude DOUBLE,
  PRIMARY KEY (product_id)
);