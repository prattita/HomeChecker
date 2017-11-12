from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
#import plotly

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DASP_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##TABLES
class LightEvent(db.Model):
    __tablename__ = 'lightEvents'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    light_level = db.Column(db.Integer)

    def __repr__(self):
        return "LightEvent(name={}, id={}, timestamp={}, light_level={})".format(
            self.name, self.id, self.timestamp, self.light_level)


class TemperatureEvent(db.Model):
    __tablename__ = 'temperatureEvent'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    temp_level = db.Column(db.Integer)

    def __repr__(self):
        return "TemperatureEvent(name={}, id={}, timestamp={}, temp_level={})".format(
            self.name, self.id, self.timestamp, self.temp_level)


@app.route('/')
@app.route('/home')#?
def show_homepage():
    light_statuses = {}
    temp_statuses = {}

    query1 = db.session.query(LightEvent.name.distinct().label("name"))
    for row in query1.all():
        light_statuses[row.name] = is_light_on(row.name)

    query2 = db.session.query(TemperatureEvent.name.distinct().label("name"))
    for row in query2.all():
        temp_statuses[row.name] = current_temp(row.name)

    return render_template('home.html',light_sensors=light_statuses,temp_sensors=temp_statuses)


def make_tables():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route("/api/light", methods=['POST'])
def get_light_event():
    body = request.get_json()
    """example body:
    {
        'name': "SensorL1",
        'timestamp': <some DateTime thing>,
        'light_level': 255,
    }
    """
    name = body['name']
    timestamp = body['timestamp']
    light_level = body['light_level']
    le = LightEvent(name=name, timestamp=timestamp, light_level=light_level)
    db.session.add(le)
    db.session.commit()
    return "OK", 200


@app.route("/api/temp", methods=['POST'])
def get_temp_event():
    body = request.get_json()
    """example body:
    {
        'name': "SensorL1",
        'timestamp': <some DateTime thing>,
        'temp_level': 255,
    }
    """
    name = body['name']
    timestamp = body['timestamp']
    temp_level = body['temp_level']
    t = TemperatureEvent(name=name, timestamp=timestamp, temp_level=temp_level)
    db.session.add(t)
    db.commit()
    return "OK", 200

def is_light_on(light_name):
    current_light = LightEvent.query.filter_by(name=light_name).first()
    if current_light.light_level > 30:
        return "ON"
    return "OFF"

def current_temp(temp_name):
    return TemperatureEvent.query.filter_by(name=temp_name).first()


@app.route('/light/<string:name>')
def show_light_info(name):
    pass


if __name__ == '__main__':
    app.run(debug=True)
