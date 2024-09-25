from models     import model as Model
from datetime   import datetime
from flask      import Blueprint, request
from extensions import flask_app, Response

simple_routes = Blueprint('simple_routes', __name__)

@simple_routes.route('/hello', methods=['GET'])
def hi():
    resp = Response()

    if request.method == 'GET':
        flask_app.log_request(request)
        try:
            resp.msg     = f'Hello'
            resp.data    = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
            resp.success = True
        except Exception as e:
                resp.msg     = f'Error: {e}'
                resp.success = False
                flask_app.debug_response(resp._msg, e)

        return flask_app._respond(request, **resp.serialize())

@simple_routes.route('/is_alive', methods=['GET'])
def im_alive():
    resp = Response()

    if request.method == 'GET':
        flask_app.log_request(request)
        try:
            resp.msg     = f'I am alive'
            resp.data    = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
            resp.success = True
        except Exception as e:
                resp.msg     = f'Error: {e}'
                resp.success = False
                flask_app.debug_response(resp._msg, e)

        return flask_app._respond(request, **resp.serialize())