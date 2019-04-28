import os

import requests
from flask import Blueprint, abort, render_template, request

from app.datapoint_client.client import DatapointClient
from app.datapoint_client.errors import SiteError
from app.site_dao import dao_get_all_sites_with_observations, dao_get_observation_search_results, dao_get_site_by_id


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/observations')
def all_site_observations():
    sites = dao_get_all_sites_with_observations()
    return render_template('observation_sites.html', sites=sites)


@main.route('/observations/<int:site_id>')
def site_observation(site_id):
    client = DatapointClient(os.getenv('DATAPOINT_API_KEY'))

    try:
        obs = client.get_obs_for_site(site_id)
    except SiteError:
        abort(404)
    except requests.exceptions.HTTPError as e:
        _abort_with_appropriate_error(e)

    site_name = dao_get_site_by_id(site_id).name

    return render_template('observation_single_site.html', obs=obs, site_name=site_name)


@main.route('/results')
def results():
    term = request.args.get('search-term')
    result = dao_get_observation_search_results(term)
    return render_template('results.html', term=result)


def _abort_with_appropriate_error(e):
    if e.response.status_code == 403:
        abort(403)
    elif e.response.status_code == 404:
        abort(404)
    else:
        abort(500)


@main.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@main.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
