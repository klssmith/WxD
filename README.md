# WxD Prototype

This is an app that displays observations and forecasts from the Met Office DataPoint service.

## Set up

### Set the environment variables

You will need to set these environment variables:

```
export FLASK_APP=application.py
export DATAPOINT_API_KEY=<datapoint-api-key>
```

You can get an API key from the [Met Office DataPoint site](https://www.metoffice.gov.uk/datapoint/api)

If running the app locally you will also need to set

```
export FLASK_ENV=development
```

### Create the database


The app needs a PostgreSQL database in order to run. Create a database - by default, the app expects to find a database
called `wxd` at this URI - `postgresql://localhost/wxd`. You can change that by setting the `SQLALCHEMY_DATABASE_URI`
environment variable.

Run the migrations to create the tables: `flask db upgrade`.

### Import the data

Make sure that you have followed the steps above, then run the `import_data` function found in `app/data_import.py`.

## Running the app

Once the stages above have been completed, `flask run` will start the app running at `http://localhost:5000`
