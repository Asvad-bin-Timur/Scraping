# Mentorship Project

## KinoPoisk Parser
At this stage, I have created a Kinopoisk parser that collects data on the top 250 movies. The script uses the KinoPoisk class from scraper.py file to scrape data from the website. The script finds links to all movies on the website and then extracts information about each movie by visiting their pages. The extracted data is then cleaned and processed using methods from Data_processing.py file. All the actions mentioned above are performed by running the main.py script.
## Data EDA
This part of the project includes the data exploratory data analysis (EDA) of the KinoPoisk dataset. The dataset is retrieved from the PostgreSQL database created in the KinoPoisk Parser script. The main purpose of this part of the project is to gain insights from the data. The EDA analysis was performed using Jupyter Notebook and presented in Notebook.ipynb.
## Dashboard
This part of the project is a web-based dashboard that displays the data from the KinoPoisk dataset. The dashboard is created using Dash from Plotly and implemented in the Dashboard.py file. The dashboard allows users to interact with the data by applying filters and selecting the desired data range.
## SQLite
SQLite is used as the database for storing the KinoPoisk dataset. The database is created using the create_db_table() function in the KinoPoisk Parser script. The script uses SQLite to create the database and the films_data table. The table stores the cleaned and processed data from the KinoPoisk website.
## Docker
In order to allow anyone to view and interact with the dashboard, a Dockerfile has been created. Here is the instruction:
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
