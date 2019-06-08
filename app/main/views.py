import requests
from flask import Blueprint, abort, render_template, request
from flask.views import View

from app import client
from app.datapoint_client.errors import SiteError
from app.models import Site
from app.site_dao import (
    dao_find_sites_by_name,
    dao_find_observation_sites_by_name,
    dao_get_all_sites,
    dao_get_all_sites_with_observations,
    dao_get_site_by_id,
)


main = Blueprint('main', __name__)


class ShowSites(View):
    template = ''

    def dispatch_request(self):
        sites = self.get_sites()
        return render_template(self.template, sites=sites)

    def get_sites(self):
        raise NotImplementedError()


class ShowObs(ShowSites):
    template = 'observation_sites.html'

    def get_sites(self):
        return dao_get_all_sites_with_observations()


class ShowForecasts(ShowSites):
    template = 'forecast_sites.html'

    def get_sites(self):
        return dao_get_all_sites()


main.add_url_rule('/observations/', view_func=ShowObs.as_view('all_site_observations'))
main.add_url_rule('/forecasts/', view_func=ShowForecasts.as_view('all_site_forecasts'))


class ShowSingleSite(View):
    template = ''
    headings = ''

    def dispatch_request(self, site_id):
        data = self.get_data(site_id)
        site = self.get_site(site_id)
        return render_template(self.template, headings=self.headings, data=data, site=site)

    def get_site(self, site_id):
        return dao_get_site_by_id(site_id)

    def get_data(self, site_id):
        raise NotImplementedError()


class ShowSingleOb(ShowSingleSite):
    template = 'observation_single_site.html'
    headings = [
        ('Date', ''),
        ('Weather', 'Weather Type'),
        ('Temperature, °C', 'Temperature'),
        ('Dew point, °C', 'Dew Point'),
        ('Relative humidity, %', 'Screen Relative Humidity'),
        ('Wind, mph', 'Wind Speed'),
        ('Wind Gust, mph', 'Wind Gust'),
        ('Pressure, hPa', 'Pressure'),
        ('Visibility, m', 'Visibility'),
    ]

    def get_data(self, site_id):
        try:
            obs = client.get_obs_for_site(site_id)
        except SiteError:
            abort(404)
        except requests.exceptions.HTTPError as e:
            _abort_with_appropriate_error(e)

        return obs


class ShowSingleForecast(ShowSingleSite):
    template = 'forecast_single_site.html'
    headings = [
        ('Date', ''),
        ('Weather', 'Weather Type'),
        ('Temperature, °C', 'Temperature'),
        ('Feels like temperature, °C', 'Feels Like Temperature'),
        ('Relative humidity, %', 'Screen Relative Humidity'),
        ('Probability of precipitation, %', 'Precipitation Probability'),
        ('Wind, mph', 'Wind Speed'),
        ('Wind Gust, mph', 'Wind Gust'),
        ('Visibility, m', 'Visibility'),
        ('Max UV Index', 'Max UV Index')
    ]

    def get_data(self, site_id):
        try:
            forecast = client.get_3hourly_forecasts_for_site(site_id)
        except SiteError:
            abort(404)
        except requests.exceptions.HTTPError as e:
            _abort_with_appropriate_error(e)

        return forecast


main.add_url_rule('/observations/<int:site_id>', view_func=ShowSingleOb.as_view('site_observation'))
main.add_url_rule('/forecasts/<int:site_id>', view_func=ShowSingleForecast.as_view('site_forecast'))


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/sites/<int:site_id>')
def site(site_id):
    site = Site.query.get_or_404(site_id)

    return render_template('site_details.html', site=site)


@main.route('/results')
def results():
    search_term = request.args.get('search-term')
    obs = request.args.get('obs')
    link = request.args.get('link')

    if obs == 'true':
        results = dao_find_observation_sites_by_name(search_term)
    else:
        results = dao_find_sites_by_name(search_term)

    results_link, back_link = get_results_page_links(link)

    return render_template('results.html', results=results, link=results_link, back_link=back_link)


def get_results_page_links(link):
    result_link = {'site': 'main.site',
                   'obs': 'main.site_observation',
                   'fx': 'main.site_forecast'}

    back_link = {'site': 'main.index',
                 'obs': 'main.all_site_observations',
                 'fx': 'main.all_site_forecasts'}

    return result_link[link], back_link[link]


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
