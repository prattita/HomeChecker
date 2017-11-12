from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DASP_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def show_homepage():
    return render_template('index.html')

##TABLES
class LightEvent(db.Model):
    __tablename__ = 'lightEvents'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    light_level = db.Column(db.Integer)

    # def __repr__(self):
    # 	return "<Book(title='%s', author=%s)" % (self.title, self.author)
    def __init__(self, name, id, timestamp, light_level):
        self.name = name
        self.id = id
        self.timestamp = timestamp
        self.light_level = light_level

class TemperatureEvent(db.Model):
    __tablename__ = 'temperatureEvent'
    name = db.Column(db.String(20), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    temp_level = db.Column(db.Integer)

    def __init__(self, name, id, timestamp, temp_level):
        self.name = name
        self.id = id
        self.timestamp = timestamp
        self.temp_level = temp_level

def make_tables():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route("/api/light", methods=['POST'])
def get_light_event():
    body = request.get_json()
    """example body:
    {
    	'name': "SensorL1"
    	'id': 123,
    	'timestamp': <some DateTime thing>,
    	'light_level': 255,
    }
    """
    name = body['name']
    id = body['id']
    timestamp = body['timestamp']
    light_level = body['light_level']
    l = LightEvent(name=name, id=id, timestamp=timestamp, light_level=light_level)
    db.session.add(l)
    db.commit()
    return "OK", 200

@app.route("/api/temp", methods=['POST'])
def get_temp_event():
    body = request.get_json()
    """example body:
    {
    	'name': "SensorL1"
    	'id': 123,
    	'timestamp': <some DateTime thing>,
    	'temp_level': 255,
    }
    """
    name = body['name']
    id = body['id']
    timestamp = body['timestamp']
    temp_level = body['temp_level']
    t = TemperatureEvent(name=name, id=id, timestamp=timestamp, temp_level=temp_level)
    db.session.add(t)
    db.commit()
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
