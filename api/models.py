from app import db


class CityTemperature(db.Model):
    __tablename__ = 'city_temperature'

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.Date)
    temperature = db.Column(db.Float)
    uncertainty = db.Column(db.Float)
    city = db.Column(db.String)
    country = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)

    def __repr__(self):
        return f'{self.id}: {self.city} - {self.temperature}°'