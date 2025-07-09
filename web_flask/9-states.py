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

@app.route('/states', strict_slashes=False)
def states():
    """Fetch all states and their cities, sorted by name, then render."""
    all_states = storage.all(State).values()
    states = sorted(all_states, key=lambda s: s.name)
    return render_template('9-states.html', states=states)

@app.route('/states/<state_id>', strict_slashes=False)
def show_state(state_id):
    """Display a single state and its cities, or 404 if not found."""
    state = storage.all(State).get(f"State.{state_id}")
    if not state:
        return render_template('9-states.html'), 404
    cities = sorted(state.cities, key=lambda c: c.name)
    return render_template('9-states.html', state=state, cities=cities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
