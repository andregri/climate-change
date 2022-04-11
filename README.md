# Climate Change API
This repo contains a restful API implemented with **Python Flask** to explore
the monthly average temperatures of cities around the world.

The dataset is loaded in a **Postgresql** database. I chose Postgresql because it is open-source.
If necessary, it can be extended with PostGIS to manage geographic objects such as latitudes
and longitudes. However, **MySQL** could have been another possible choice.

The backend server and the database are containerized using **Docker** and **docker-compose**.
For the database image, I copied a `.sql` file with the instructions to create a table and
copying the data from the `.csv` file. These instructions are executed when docker-compose
starts a container from the database image. Since the api container depends on the
database container, I needed a way to know when the database server was ready to accept connections.
I partially solved this issue by adding a healthcheck that probes if the database is created.

For documenting the API I chose **Flasgger** because is easy to use with Flask and
provides a nice SwaggerUI to visualize and test the routes.

# Requirements
Download and extract the dataset [GlobalLandTemperaturesByCity.csv](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data?select=GlobalLandTemperaturesByCity.csv) into `db` folder.

# Installation
Open a terminal and cd to the folder in which `docker-compose.yml` is saved.

## Running containers
To build and start containers run:
```
docker-compose up --build
```

Note that the **first time** you build the containers, the database initialization
may take few minutes. Wait few minutes before using the API.

## Stopping containers
To stop containers run:
```
docker-compose down
```

To also remove docker volumes run:
```
docker-compose down -v
```

# Documentation
The API documentation is generated with [Swagger](https://github.com/flasgger/flasgger)
and it is visible at [/apidocs](http://127.0.0.1:5000/apidocs)

# Examples
## Question A
Find the entry whose city has the highest AverageTemperature since the year 2000.

You can do the request from Flasgger or from curl:
```
curl -X POST "http://127.0.0.1:5000/top" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"end_date\": \"2022-05-01\",  \"n\": 1,  \"start_date\": \"2000-01-01\"}"
```

Response body:
```
[
  {
    "city": "Ahvaz",
    "country": "Iran",
    "dt": "Mon, 01 Jul 2013 00:00:00 GMT",
    "latitude": "31.35N",
    "longitude": "49.01E",
    "temperature": 39.15600000000001,
    "uncertainty": 0.37
  }
]
```

## Question B
Following question A: assume the temperature observation of the city last month breaks the record. It is 0.1 degree higher with the same uncertainty. Create this entry.

Curl request:
```
curl -X POST "http://127.0.0.1:5000/temp" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"city\": \"Ahvaz\",  \"country\": \"Iran\",  \"dt\": \"2022-03-01\",  \"latitude\": \"31.35N\",  \"longitude\": \"49.01E\",  \"temperature\": 39.256,  \"uncertainty\": 0.37}"
```

Response body with status code 201:
```
{
  "city": "Ahvaz",
  "country": "Iran",
  "dt": "Tue, 01 Mar 2022 00:00:00 GMT",
  "latitude": "31.35N",
  "longitude": "49.01E",
  "temperature": 39.256,
  "uncertainty": 0.37
}
```

## Question C
Following question A: assume the returned entry has been found erroneous. The actual average temperature of this entry is 2.5 degrees lower. Update this entry.

Curl request:
```
curl -X POST "http://127.0.0.1:5000/temp" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"city\": \"Ahvaz\",  \"country\": \"Iran\",  \"dt\": \"2013-07-01\",  \"latitude\": \"31.35N\",  \"longitude\": \"49.01E\",  \"temperature\": 36.656,  \"uncertainty\": 0.37}"
```

Response body with status code 200:
```
{
  "city": "Ahvaz",
  "country": "Iran",
  "dt": "Mon, 01 Jul 2013 00:00:00 GMT",
  "latitude": "31.35N",
  "longitude": "49.01E",
  "temperature": 36.656,
  "uncertainty": 0.37
}
```

# Hours needed
| Day | Hours |
|:---|---:|
| Wednesday 6 | 2 |
| Thursday 7 | 1 |
| Friday 8 | 3 |
| Saturday 9 | 1 |
| Sunday 10 | 3 |
| Monday 11 | 2 |
| **Total** | **12** |