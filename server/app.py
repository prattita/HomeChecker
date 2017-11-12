from flask import *

app = Flask(__name__, static_url_path='')


@app.route('/')
def show_homepage():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
