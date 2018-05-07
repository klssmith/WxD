import os

import requests
from flask import abort, render_template

from app import app
from app.datapoint_client.client import DatapointClient
from app.datapoint_client.errors import SiteError
from app.site_dao import dao_get_all_sites_with_observations, dao_get_site_by_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/observations')
def all_site_observations():
    sites = dao_get_all_sites_with_observations()
    return render_template('observation_sites.html', sites=sites)


@app.route('/observations/<int:site_id>')
def site_observation(site_id):
    client = DatapointClient(os.getenv('DATAPOINT_API_KEY'))

    try:
        obs = client.get_all_obs_for_site(site_id)
    except SiteError:
        abort(404)
    except requests.exceptions.HTTPError as e:
        _abort_with_appropriate_error(e)

    site_name = dao_get_site_by_id(site_id).name

    return render_template('observation_single_site.html', obs=obs, site_name=site_name)


def _abort_with_appropriate_error(e):
    if e.response.status_code == 403:
        abort(403)
    elif e.response.status_code == 404:
        abort(404)
    else:
        abort(500)


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
