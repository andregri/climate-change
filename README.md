# Climate Change API

## Requirements
Download the dataset [GlobalLandTemperaturesByCity.csv](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data?select=GlobalLandTemperaturesByCity.csv) into `db` folder.

## Installation
Open a terminal and cd to the folder in which `docker-compose.yml` is saved.

### Running containers
To build and start containers run:
```
docker-compose up --build
```

Note that the **first time** you build the containers, the database initialization
may take few minutes. Wait few minutes before using the API.

### Stopping containers
To stop containers run:
```
docker-compose down
```

To also remove docker volumes run:
```
docker-compose down -v
```

## Documentations
The API documentation is generated with [Swagger](https://github.com/flasgger/flasgger)
and it is visible at [http://127.0.0.1:5000/apidocs]()