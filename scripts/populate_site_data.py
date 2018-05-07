from app import db
from app.models import Site
from app.site_dao import dao_get_site_by_id


def add_sites_to_database(data):
    '''
    This function takes the list of sites for which forecast data is available and creates an entry in the database for
    each site.

    The argument <data> is the raw content of this endpoint:
    http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=<API key>
    '''

    places = data['Locations']['Location']
    for place_dict in places:
        site = Site()

        site.id = int(place_dict['id'])
        site.name = place_dict['name']
        site.latitude = float(place_dict['latitude'])
        site.longitude = float(place_dict['longitude'])
        if 'elevation' in place_dict:
            site.elevation = float(place_dict['elevation'])
        if 'region' in place_dict:
            site.region = place_dict['region']
        if 'unitaryAuthArea' in place_dict:
            site.unitary_auth_area = place_dict['unitaryAuthArea']
        if 'obsSource' in place_dict:
            site.obs_source = place_dict['obsSource']
        if 'nationalPark' in place_dict:
            site.national_park = place_dict['nationalPark']

        db.session.add(site)
        print('Adding {}'.format(site.name))

    db.session.commit()


def mark_sites_which_have_observations(data):
    '''
    This function takes the list of sites for which observation data is available and updates the database entry for
    that site to mark it as having observations.

    This function can only be run once the forecast sites are already in the database.

    The argument <data> is the raw content of this endpoint:
    http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/sitelist?key=<API key>
    '''

    places = data['Locations']['Location']

    for place_dict in places:
        original_site = dao_get_site_by_id(int(place_dict['id']))

        original_site.observations = True
        db.session.add(original_site)
        print('Updating {}'.format(original_site.name))

    db.session.commit()
