#!/usr/bin/python3
"""a script that starts a flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ a function that prints hello `hbnb at the root"""
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
