import json
from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, and_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andrea:password@db:5432/climate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import CityTemperature


@app.route('/temp', methods=['POST'])
def create():
    request_data = request.get_json()
    date = request_data['date']
    temp = request_data['temperature']
    unct = request_data['uncertainty']
    city = request_data['city']
    cnty = request_data['country']
    llat = request_data['latitude']
    long = request_data['longitude']

    new_temp = CityTemperature(dt=date, temperature=temp, uncertainty=unct,
        city=city, country=cnty, latitude=llat, longitude=long)

    db.session.add(new_temp)
    db.session.commit()
    
    res = make_response(jsonify({"message": f"Row {new_temp.id} created"}), 201)
    return res

@app.route('/temp/<int:id>', methods=['GET'])
def get_by_id(id):
    temp = CityTemperature.query.filter_by(id=id).first()
    return str(temp)

@app.route('/temp', methods=['PATCH'])
def update():
    request_data = request.get_json()
    city = request_data['city']
    date = request_data['date']
    temp = request_data['temperature']
    unct = request_data['uncertainty']

    row = CityTemperature.query.filter_by(city=city, dt=date).first()
    if row:
        row.temperature = temp
        row.uncertainty = unct
        res = make_response(jsonify({"message": f"Row {row.id} updated"}), 200)
        
    else:
        new_row = CityTemperature(dt=date, temperature=temp, uncertainty=unct, city=city)
        db.session.add(new_row)
    
    db.session.commit()
    return res

@app.route('/top', methods=['GET'])
def top():
    request_data = request.get_json()
    n = request_data['n']
    if n and n <= 0:
        return make_response(jsonify({'message': 'Invalid n'}), 400)

    start_date = request_data['start_date']
    end_date = request_data['end_date']
    if start_date >= end_date:
        return make_response(jsonify({'message': 'end_date must be later the start_date'}), 400)

    subq = db.session.query(
            func.max(CityTemperature.temperature).label('max_temp'),
            CityTemperature.city
        ) \
        .filter(CityTemperature.dt >= start_date) \
        .filter(CityTemperature.dt <= end_date) \
        .group_by(CityTemperature.city) \
        .order_by(desc('max_temp')) \
        .limit(n) \
        .subquery()

    top_temperatures = db.session.query(CityTemperature). \
        join(subq, and_(CityTemperature.city==subq.c.city, CityTemperature.temperature==subq.c.max_temp)). \
        order_by(desc(CityTemperature.temperature)).all()

    return make_response(jsonify(top_temperatures), 200)


if __name__ == '__main__':
    app.run()