from enum import Enum

class HTTPStatusCode(Enum):
    OK           = 200
    CREATED      = 201
    BAD_REQUEST  = 400
    NOT_FOUND    = 404
    SERVER_ERROR = 500

    @classmethod
    def to_dict(self):
        return dict(HTTPStatusCode.__members__)