import os

from flask import abort, render_template

from app import app
from app.datapoint_client.client import DatapointClient
from app.datapoint_client.errors import SiteError


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/observations/<int:site_id>')
def site_observation(site_id):
    client = DatapointClient(os.getenv('DATAPOINT_API_KEY'))

    try:
        obs = client.get_all_obs_for_site(site_id)
    except SiteError:
        abort(404)

    return render_template('observation_single_site.html', obs=obs)
