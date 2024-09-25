#### PREVENT PYCACHE ####
import sys
sys.dont_write_bytecode = True

#### ADD PYTHONPATH ####
sys.path.append('/tools/python/packages/lib/python3.6/site-packages/')
# sys.path.append('/usr/local/lib64/python3.6/site-packages')

from extensions.setup import app, db, FlaskApp, Response
from extensions.constants import HTTPStatusCode

flask_app = FlaskApp()