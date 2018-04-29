from app import db
from app.models import Site


def add_data(data):
    '''
    The argument <data> should be the raw content of this endpoint:
    http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=<API key>
    The simplest way to run this function is to paste the contents of the endpoint above into a file, then use the file
    content as the argument.
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
