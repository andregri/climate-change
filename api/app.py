from flask import Flask, request, make_response, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func, and_
from flasgger import Swagger, swag_from


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andrea:password@db:5432/climate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
swagger = Swagger(app)

from models import CityTemperature


@app.route('/temp', methods=['POST'])
@swag_from('./docs/post_temp.yml')
def create():
    request_data = request.get_json()

    if not 'dt' in request_data:
        return make_response(jsonify({'message': 'You must specify a value for dt'}), 400)
    
    if not 'city' in request_data:
        return make_response(jsonify({'message': 'You must specify a value for city'}), 400)

    date = request_data['dt']
    city = request_data['city']
    row = CityTemperature.query.filter_by(city=city, dt=date).first()
    if row:
        try:
            row.temperature = request_data['temperature']
            row.uncertainty = request_data['uncertainty']
        except ValueError as e:
            res = make_response(jsonify({'message': str(e)}), 400)
        else:
            db.session.commit()
            res = make_response(jsonify(row), 200)
        
    else:
        try:
            new_row = CityTemperature(**request_data)
        except ValueError as e:
            res = make_response(jsonify({'message': str(e)}), 400)
        else:
            db.session.add(new_row)
            db.session.commit()
            res = make_response(jsonify(new_row), 201)

    return res

@app.route('/top', methods=['POST'])
@swag_from('./docs/top.yml')
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

@app.route('/')
def index():
    return redirect('apidocs', code=303)

if __name__ == '__main__':
    app.run()