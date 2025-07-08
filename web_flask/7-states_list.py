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

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Render a list of all State objects sorted by name."""
    all_states = storage.all(State).values()
    states = sorted(all_states , key=lambda s: s.name)
    return render_template('7-states_list.html', states=states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
