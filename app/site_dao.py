from app.models import Site


def dao_get_site_by_id(site_id):
    return Site.query.get(site_id)
