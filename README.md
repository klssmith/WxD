# WxD Prototype

This is an app that displays observations and forecasts from the Met Office DataPoint service.

## Running the application

You will need to set these environment variables:

```
export FLASK_APP=wxd.py
export DATAPOINT_API_KEY=<datapoint-api-key>
```

### Importing the data

The app needs a PostgreSQL database in order to run. Create a database - by default, the app will look for a database
called `wxd` at this URI - `postgresql://localhost/wxd`. You can change that by setting the `SQLALCHEMY_DATABASE_URI`
environment variable.

Run the migrations to create the tables.

Use the `add_data` function located in `scripts/populate_site_data.py` to populate the site data. You can find
instructions on using the function in its docstring.
