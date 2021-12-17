
from flask import Flask
import os


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return 'World Hello!'


if __name__ == '__main__':
    app.run()
