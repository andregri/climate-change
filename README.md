# Climate Change API
A restful API implemented with **Python Flask** to navigate the monthly average temperatures of cities in the world.

The dataset is loaded in a **Postgresql** database.

The backend server and the database are containerized using **Docker** and **docker-compose**.

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

Curl request:
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
    "id": 117010,
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
curl -X POST "http://127.0.0.1:5000/temp" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{    \"city\": \"Ahvaz\",    \"country\": \"Iran\",    \"dt\": \"2022-03-01\",    \"latitude\": \"31.35N\",    \"longitude\": \"49.01E\",    \"temperature\": 39.25600000000001,    \"uncertainty\": 0.37}"
```

Response body:
```
{
  "message": "Row 8599213 created"
}
```

## Question C
Following question A: assume the returned entry has been found erroneous. The actual average temperature of this entry is 2.5 degrees lower. Update this entry.

Curl request:
```
curl -X POST "http://127.0.0.1:5000/temp" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{    \"city\": \"Ahvaz\",    \"country\": \"Iran\",    \"dt\": \"2013-07-01\",    \"latitude\": \"31.35N\",    \"longitude\": \"49.01E\",    \"temperature\": 36.656,    \"uncertainty\": 0.37}"
```

Response body:
```
{
  "message": "Row 117010 updated"
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
| Monday 11 | |
| **Total** | **10** |