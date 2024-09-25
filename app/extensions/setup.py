import os, logging
from flask                  import Flask
from pathlib                import Path
from copy                   import deepcopy
from datetime               import datetime
from dotenv                 import load_dotenv
from flask_sqlalchemy       import SQLAlchemy
from extensions.constants   import HTTPStatusCode

app = Flask(__name__)

load_dotenv()

DB_SERVER   = os.getenv('%API_TITLE_UPPER_DB_SERVER')
DB_USER     = os.getenv('%API_TITLE_UPPER_DB_USER')
DB_PASSWORD = os.getenv('%API_TITLE_UPPER_DB_PASSWORD')
DB_SCHEMA   = os.getenv('%API_TITLE_UPPER_DB_SCHEMA')

app.config['CACHE_TYPE']                     = os.getenv('CACHE_TYPE')
app.config['SQLALCHEMY_ECHO']                = False
app.config['SQLALCHEMY_DATABASE_URI']        = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_SCHEMA}'
app.config['SQLALCHEMY_RECORD_QUERIES']      = False
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.session.begin(subtransactions=True)

class FlaskApp:
    def __init__(self) -> None:
        self.setup()

    def setup(self):
        self.config_logger()
        self.info(f'Flask server started on {os.getenv("HOSTNAME")}')

    def config_logger(self):
        if os.getenv('DEV_LOG_DIR'):
            log_path = os.path.join(os.getenv('DEV_LOG_DIR'), '%API_TITLE_dev.log')
        elif os.getenv('LOG_DIR'):
            log_path = os.path.join(os.getenv('LOG_DIR'), '%API_TITLE_flask.log')
        else:
            curr_path = os.path.abspath(__file__)
            path_obj  = Path(curr_path)
            directory = path_obj.parent.parent
            log_path  = directory / 'logs/%API_TITLE_flask.log'

        logging.basicConfig(
            format   ='%(asctime)s %(levelname)s: %(message)s',
            level    = logging.DEBUG,
            filename = log_path
            )
        log = logging.getLogger()

        self.info  = log.info
        self.error = log.error
        self.warn  = log.warn
        self.debug = log.debug

        self.debug(f'Logger configured to {log_path}')

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%a, %d %b %Y %H:%M:%S %Z')
            return True
        except:
            return False

    def resp_obj(self):
        resp_obj = {
                'success'    : False,
                'host'       : os.getenv('HOSTNAME'),
                'status_code': HTTPStatusCode.NOT_FOUND.value,
            }
        
        return deepcopy(resp_obj)
    
    def success(self, *args, **kwargs):
        resp_obj = self.resp_obj()
        resp_obj.update(
            {
                'success': True,
                'status_code': HTTPStatusCode.OK.value,
                **kwargs
            }
        )

        if kwargs['msg']:
            self.info(kwargs['msg'])

        return resp_obj

    def failure(self, *args, **kwargs):
        resp_obj = self.resp_obj()
        resp_obj.update(
            {
                'success': False,
                'status_code': HTTPStatusCode.NOT_FOUND.value,
                **kwargs
            }
        )

        if kwargs['msg']:
            self.error(kwargs['msg'])

        return resp_obj
    
    def _respond(self, request, **kwargs):
        msg     = kwargs.pop('msg', str())
        data    = kwargs.pop('data', dict())
        # in_cache= kwargs.pop('in_cache', False)
        success = kwargs.pop('success', False)

        if not request:
            msg  = 'Request body not found'
            resp = self.failure(**{'msg': msg})
        if success and request:
            msg  = f'{request.method} {request.url_rule.rule} succeeded : {msg}'
            if data:
                resp = self.success(**{'msg': msg, 'data': data})
            else:
                resp = self.success(**{'msg': msg})
        elif not success and request:
            msg  = f'{request.method} {request.url_rule.rule} failed : {msg}'
            resp = self.failure(**{'msg': msg})

        return resp, resp['status_code']

    def respond(self, request, msg, data, success):
        if success :
            msg  = f'{request.method} {request.url_rule.rule} succeeded : {msg}'
            if data:
                resp = self.success(**{'msg': msg, 'data': data})
            else:
                resp = self.success(**{'msg': msg})
        else:
            msg  = f'{request.method} {request.url_rule.rule} failed : {msg}'
            resp = self.failure(**{'msg': msg})

        return resp, resp['status_code']

    def log_request(self, request):
        self.info(f'{request.method} {request.url_rule.rule} accessed by {request.remote_addr}')

    def debug_response(self, msg: str = str(), error: str = str()):
        self.debug(msg)
        self.debug(error)

class Response:
    def __init__(self):
        self._msg     = str()
        self._data    = dict()
        # self._in_cache= bool(False)
        self._success = bool(False)

    def set_success(self):
        self._success = True

    def set_failure(self):
        self._success = False

    # def set_in_cache(self):
    #     self._in_cache = True

    def set_msg(self, msg):
        self._msg = msg

    def set_data(self, data):
        self._data = data

    @property
    def to_dict(self):
        return {
            'msg'     : self._msg,
            'data'    : self._data,
            'success' : self._success,
        }

    def serialize(self):
        return {
            'msg'     : self._msg,
            'data'    : self._data,
            'success' : self._success,
            # 'in_cache': self._in_cache
        }
    
    # GETTERS AND SETTERS #

    @property
    def msg(self):
        return self._msg
    
    @msg.setter
    def msg(self, value):
        self._msg = value


    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value


    @property
    def success(self):
        return self._success
    
    @success.setter
    def success(self, value):
        self._success = value
