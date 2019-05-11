from app import db


class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)
    region = db.Column(db.String(100))
    unitary_auth_area = db.Column(db.String(100))
    obs_source = db.Column(db.String(100))
    national_park = db.Column(db.String(100))
    observations = db.Column(db.Boolean, nullable=False, index=True, default=False)

    def __repr__(self):
        return '<Site: {} {}>'.format(self.id, self.name)
