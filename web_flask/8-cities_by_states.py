#!/usr/bin/env python
import sys
import os
from flask import Flask, render_template
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy Session after each request."""
    storage.close()

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Fetch all states and their cities, sorted by name, then render."""
    all_states = storage.all(State).values()
    states = sorted(all_states, key=lambda s: s.name)
    return render_template('8-cities_by_states.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
