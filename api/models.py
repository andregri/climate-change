from dataclasses import dataclass
from datetime import date
from app import db
from sqlalchemy.orm import validates


@dataclass
class CityTemperature(db.Model):
    __tablename__ = 'city_temperature'
    dt: date
    temperature: float
    uncertainty: float
    city: str
    country: str
    latitude: str
    longitude: str

    dt = db.Column(db.Date, primary_key=True)
    temperature = db.Column(db.Float)
    uncertainty = db.Column(db.Float)
    city = db.Column(db.String, primary_key=True)
    country = db.Column(db.String)
    latitude = db.Column(db.String, primary_key=True)
    longitude = db.Column(db.String, primary_key=True)

    @validates('temperature')
    def validate_temperature(self, key, temp):
        if temp < -273.15:
            raise ValueError("Invalid temperature")
        return temp
    
    @validates('uncertainty')
    def validate_uncertainty(self, key, uncertainty):
        if uncertainty < 0:
            raise ValueError("Invalid uncertainty")
        return uncertainty

    def __repr__(self):
        return f"""
            {self.dt}, {self.temperature}, {self.uncertainty}, {self.city}
        """