from datetime   import datetime
from models     import model as Model
from flask      import Blueprint, request
from extensions import db, flask_app, Response
from sqlalchemy import or_, and_, func, case, delete

db_routes = Blueprint('db_routes', __name__)

@db_routes.route('/entry', methods=['GET', 'POST', 'PATCH'])
def row():
    resp = Response()

    if request.method == 'GET': # GET ROW
        flask_app.log_request(request)

        try:
            row_id = request.form.get('id', None)
            if row_id:
                row = Model.query.filter_by(id = row_id).first()
                if row:
                    row_data = row.as_dict
                    
                    resp.msg     = f'Found row {row_id} in database'
                    resp.data    = row_data
                    resp.success = True
            else:
                resp.msg     = f'ID not provided'
                resp.success = False
        except Exception as e:
                resp.msg     = f'Error finding submit_job {row_id}: {e}'
                resp.success = False
                flask_app.debug_response(resp._msg, e)

        return flask_app._respond(request, **resp.serialize())
    
    if request.method == 'POST': # NEW ROW
        flask_app.log_request(request)
        
        try:
            row = Model(
                **{ col: request.form.get(col, None) for col in Model().columns }
            )

            db.session.add(row)
            db.session.flush()
            db.session.commit()
            
            resp.msg     = f'Row {row.id} created'
            resp.data    = row.id
            resp.success = True
        
        except Exception as e:
            resp.msg     = f'Could not create row'
            resp.success = False
            flask_app.debug_response(resp._msg, e)

        return flask_app._respond(request, **resp.to_dict)

    if request.method == 'PATCH': # UPDATE JOB
        flask_app.log_request(request)
        
        try:
            row_id = request.form.get('id', None)
            if row_id:
                flask_app.debug(request.form)
                
                Model.query.filter_by(id = row_id).update(
                    { col: request.form.get(col, None) for col in Model().columns if col in request.form }
                )
                
                db.session.commit()

                resp.msg = f'Updated row {row_id}'
                resp.data = row_id
                resp.success = True

        except Exception as e:
            resp.msg = f'Error updating job {row_id}: {e}'
            resp.success = False

            flask_app.debug_response(resp._msg, e)

        return flask_app._respond(request, **resp.to_dict)