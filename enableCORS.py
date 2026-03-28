from functools import wraps
from flask import make_response


def cors_enabled(func):
    """ This decorator adds a CORS-allowing header to the response of the view it's added to. """    
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    
    return wrapper