from flask import Flask
from flask_sqlalchemy import SQLAlchemy, render_template
import os


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DASP_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route('/')
def show_homepage():
    return render_template('index.html')
    # return render_template("main.html", light=True)


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


if __name__ == '__main__':
    app.run(debug=True)
