from dataclasses import dataclass
from datetime import date
from app import db
from sqlalchemy.orm import validates


@dataclass
class CityTemperature(db.Model):
    __tablename__ = 'city_temperature'
    id: int
    dt: date
    temperature: float
    uncertainty: float
    city: str
    country: str
    latitude: str
    longitude: str

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.Date)
    temperature = db.Column(db.Float)
    uncertainty = db.Column(db.Float)
    city = db.Column(db.String)
    country = db.Column(db.String)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)

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
            {self.id}, {self.dt}, {self.temperature}, {self.uncertainty}, {self.city}
        """