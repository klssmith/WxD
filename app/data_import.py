import os

import requests

from app import db
from app.models import Site
from app.site_dao import dao_get_site_by_id


def delete_current_data():
    Site.query.delete()


def add_sites_to_database(api_key):
    forecast_sites = requests.get(
        'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={}'.format(api_key)
    ).json()

    locations = forecast_sites['Locations']['Location']
    for location in locations:
        site = Site()

        site.id = int(location['id'])
        site.name = location['name']
        site.latitude = float(location['latitude']) if location.get('latitude') else None
        site.longitude = float(location['longitude']) if location.get('longitude') else None
        site.elevation = float(location['elevation']) if location.get('elevation') else None
        site.region = location.get('region')
        site.unitary_auth_area = location.get('unitaryAuthArea')
        site.obs_source = location.get('obsSource')
        site.national_park = location.get('nationalPark')

        db.session.add(site)
        print('Adding {}'.format(site.name))


def mark_sites_which_have_observations(api_key):
    obs_sites = requests.get(
        'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist?key={}'.format(api_key)
    ).json()

    locations = obs_sites['Locations']['Location']
    for location in locations:
        site = dao_get_site_by_id(int(location['id']))
        site.observations = True

        db.session.add(site)
        print('Marking {} as a site with observations'.format(site.name))


def import_data():
    api_key = os.getenv('DATAPOINT_API_KEY')
    if not api_key:
        raise Exception('No api key found')

    delete_current_data()
    add_sites_to_database(api_key)
    mark_sites_which_have_observations(api_key)

    db.session.commit()

    print('☀️ Data import complete! ☀️')
