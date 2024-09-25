#### PREVENT PYCACHE ####
import sys
sys.dont_write_bytecode = True

from .db_routes     import db_routes
from .simple_routes import simple_routes