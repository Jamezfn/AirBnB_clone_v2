#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    """Close storage session on teardown."""
    storage.close()

@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Render the filters page with States, Cities, Amenities."""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    #cities = sorted(storage.all(City).values(), key=lambda c: c.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda a: a.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
