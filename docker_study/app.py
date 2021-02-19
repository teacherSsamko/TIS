import requests
from flask import Flask

app = Flask("api_test")

@app.route('/')
def hello():
    return 'Hello'

@app.route('/oauth')
def oauth():
    return 'good'

@app.route('/command')
def cmd():
    return 'ngrok tunnel is up and running'

@app.route('/lunch')
def lunch():
    return 'lunch time'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)