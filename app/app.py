__VERSION__ = "0.1"

import sys
sys.dont_write_bytecode = True
 
import time, os
import waitress
import werkzeug.serving

#### PRIVATE IMPORTS ####
from flask         import request, g as app_ctx
from extensions    import app, flask_app #, perf_mon
from routes        import db_routes, simple_routes


#### BLUEPRINTS ####
app.register_blueprint(db_routes)
app.register_blueprint(simple_routes)

#### RUN SERVER ####
@werkzeug.serving.run_with_reloader
def run_server():
    app.debug = True
    waitress_cfg = {
        'app': app,
        'listen': f'0.0.0.0:{os.getenv("%API_TITLE_UPPER_API_PORT", 5000)}',
        'threads': os.getenv("%API_TITLE_UPPER_API_THREADS", 4),
    }
    print(f'Serving on {os.getenv("HOSTNAME")}:{os.getenv("%API_TITLE_UPPER_API_PORT", 5000)}')
    waitress.serve(**waitress_cfg)

if __name__ == "__main__":
    run_server()