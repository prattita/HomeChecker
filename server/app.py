from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
import plotly
import json

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DASP_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# TABLES
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
def show_homepage():
    light_statuses = {}
    temp_statuses = {}

    query1 = db.session.query(LightEvent.name.distinct().label("name"))
    for row in query1.all():
        light_statuses[row.name] = is_light_on(row.name)

    query2 = db.session.query(TemperatureEvent.name.distinct().label("name"))
    for row in query2.all():
        temp_statuses[row.name] = current_temp(row.name)

    return render_template('index.html',
                           light_sensors=light_statuses,
                           temp_sensors=temp_statuses)


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
    db.session.commit()
    return "OK", 200


def is_light_on(light_name):
    current_light = LightEvent.query.filter_by(name=light_name).order_by(LightEvent.timestamp.desc()).first()
    if current_light.light_level > 100:
        return "ON"
    return "OFF"


def current_temp(temp_name):
    return TemperatureEvent.query.filter_by(name=temp_name).order_by(TemperatureEvent.timestamp.desc()).first().temp_level


@app.route('/light/<string:light_name>')
def show_light_info(light_name):
    current_light = LightEvent.query.filter_by(name=light_name).first()
    current_status = is_light_on(current_light.name)
    #current_lights = db.session.query(LightEvent).filter_by(LightEvent.name.in_((1, 2, 3, 5))).all()
    current_lights = LightEvent.query.filter_by(name=light_name).all()
    x = [row.timestamp for row in current_lights]
    y = [row.light_level for row in current_lights]

    graphs = [{
        'data': [
            {
                'x': x,
                'y': y,
                'type': 'scatter',
            }
        ],
        'layout': {'title': 'Light Sensor: Last 7 Days'},
    }]

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('light_sen.html',
                           light_name=light_name,
                           current_status=current_status,
                           ids=ids,
                           graphJSON=graphJSON)


@app.route('/temp/<string:temp_name>')
def show_temp_info(temp_name):
    c_temp_name = TemperatureEvent.query.filter_by(name=temp_name).first().name
    temp_now = current_temp(c_temp_name)
    current_temps = TemperatureEvent.query.filter_by(name=temp_name).all()
    x = [row.timestamp for row in current_temps]
    y = [row.temp_level for row in current_temps]

    graphs = [{
        'data': [
            {
                'x': x,
                'y': y,
                'type': 'scatter',
            }
        ],
        'layout': {'title': 'Temperature Sensor: Last 7 Days'},
    }]

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('temp_sen.html',
                           temp_name=c_temp_name,
                           temp_now=temp_now,
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)
