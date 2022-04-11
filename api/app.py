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

    # Check that request json body has the valus for the composite key columns,
    # otherwise return an error message.
    primary_keys = ['dt', 'city', 'latitude', 'longitude']
    if not all([k in request_data for k in primary_keys]):
        msg = 'You must specify a value for dt, city, latitude, longitude'
        return make_response(jsonify({'message': msg}), 400)

    # Update the row if it exists in the database
    row = CityTemperature.query.filter_by(**request_data).first()
    if row:
        try:
            row.temperature = request_data['temperature']
            row.uncertainty = request_data['uncertainty']
        except ValueError as e:
            res = make_response(jsonify({'message': str(e)}), 400)
        else:
            db.session.commit()
            res = make_response(jsonify(row), 200)
    # Create a new row if it does not exists in the database
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

    # Check that the request body contains all required keys
    if not all([k in request_data for k in ['n', 'start_date', 'end_date']]):
        msg = 'You must specify a value for n, start_date, end_date'
        return make_response(jsonify({'message': msg}), 400)

    # Check that request data are valid
    n = request_data['n']
    if n <= 0:
        return make_response(jsonify({'message': 'Missing or Invalid n'}), 400)

    start_date = request_data['start_date']
    end_date = request_data['end_date']
    if start_date >= end_date:
        return make_response(jsonify({'message': 'end_date must be later than start_date'}), 400)

    # Group max temperature by city and filter date between start_date and end_date.
    # Then order by max temperature and limit the number of results.
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

    # Join the subquery to get all columns
    top_temperatures = db.session.query(CityTemperature). \
        join(subq, and_(CityTemperature.city==subq.c.city, CityTemperature.temperature==subq.c.max_temp)). \
        order_by(desc(CityTemperature.temperature)).all()

    return make_response(jsonify(top_temperatures), 200)

@app.route('/')
def index():
    return redirect('apidocs', code=303)

if __name__ == '__main__':
    app.run()