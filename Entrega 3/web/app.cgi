#!/usr/bin/python3
import sys

sys.path.insert(0, "~/.local/lib/python3.9/site-packages/")

# Import the required modules
from wsgiref.handlers import CGIHandler
from web import app

# Run the Flask application using the CGIHandler
CGIHandler().run(app)
