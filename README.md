# Mentorship Project

## KinoPoisk Parser

## Data EDA

## Dashboard

## PostgreSQL

## Docker
### Build Docker Image
You should be in the project folder
```
docker build -t dash_dev .
```
### Run Docker Image
```
docker run --rm -itdp 127.0.0.1:8050:8050 --name dashboard dash_dev
```
Now the dashboard should appear on localhost:8050
### Go inside running image if needed
```
docker exec -it dashboard bash
```
