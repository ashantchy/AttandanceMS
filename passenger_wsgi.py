import sys
import os

# 1. Add your project directory to the Python path so local imports (like 'lib') work
sys.path.insert(0, os.path.dirname(__file__))

# 2. Import the WSGI adapter and your FastAPI instance from main.py
from a2wsgi import ASGIMiddleware
from main import app

# 3. Define 'application' which Phusion Passenger looks for as the entry point
application = ASGIMiddleware(app)