# exch-api
Fetches currency rates from two different sources, finds the cheapest one

## Run docker container

```shell
$ docker-compose up -d
```

Rebuild containers

```shell
$ docker-compose up --build -d
```

## Run unit tests

```shell
$ docker-compose run exchange_api python manage.py test
```