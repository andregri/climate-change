from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andrea:password@db:5432/climate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import CityTemperature


@app.route('/')
def hello():
    return str(CityTemperature.query.filter_by(id=2).first())


if __name__ == '__main__':
    app.run()