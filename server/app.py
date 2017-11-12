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


class LightEvent(db.Model):
    __tablename__ = 'lightEvents'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    light_level = db.Column(db.Integer)

    # def __repr__(self):
    # 	return "<Book(title='%s', author=%s)" % (self.title, self.author)


def make_tables():
    db.create_all()
    db.session.commit()


@app.route("/api/light", methods=['POST'])
def get_light_event():
    body = request.get_json()
    """example body:
    {
    	'id': 123,
    	'timestamp': <some DateTime thing>,
    	'light_level': 255,
    }
    """
    # pi = Pi(name=body['name'], url=body['url'])
    # db.session.merge(pi)
    # db.session.commit()
    # return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
