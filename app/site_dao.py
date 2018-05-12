from app.models import Site


def dao_get_site_by_id(site_id):
    return Site.query.get(site_id)


def dao_get_all_sites_with_observations():
    return Site.query.filter_by(
        observations=True
    ).order_by('name').all()


def dao_get_observation_search_results(term):
    return Site.query.filter(
        Site.observations == True,  # noqa
        Site.name.ilike('%{}%'.format(term))
    ).order_by('name').all()
