from flask import Flask

app = Flask(__name__, static_url_path='')


@app.route('/')
def show_homepage():
    return "wow"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
