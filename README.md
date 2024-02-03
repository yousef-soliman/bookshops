# bookshops

start the app
```console
docker-compose up -d
```
go to 
```console
http://localhost:8000/docs
```

the docker container will run the migration and start the web app service 

to run tests
```console
docker-compose exec  web pytest
```
