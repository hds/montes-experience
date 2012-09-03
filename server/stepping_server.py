import os
import json
#import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from perform_stepping import stepping_invariants, inv_article_3

#from werkzeug.routing import Map, Rule
#from werkzeug.exceptions import HTTPException, NotFound
#from werkzeug.wsgi import SharedDataMiddleware
#from werkzeug.utils import redirect
#from jinja2 import Environment, FileSystemLoader

MIME_TYPE = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/x-javascript',
    '.txt': 'text/plain',
}

def application(environ, start_response):
    request = Request(environ)

    if request.path == '/stepping/':
        
        inv_correct = False
        if 'inv' in request.args:
            print '<<<' + request.args['inv'] + '>>>'
            invars = json.loads(request.args['inv'])
            if 'hidden' in invars and 'types' in invars and 'j' in invars:
                inv_correct = True
            #print invars

        #invars = inv_article_3()
        #print json.dumps(invars)
        if inv_correct:
            res = stepping_invariants(invars)
            response = Response(res, mimetype='application/json')
        else:
            response = Response('Error 400: Invariants (?inv) incorrect', status=400)

    else:
        path = request.path
        if path == '/':
            path = '/index.html'
        path = os.path.join('../www/', path[1:])
        if os.access(path, os.R_OK):
            fd = open(path)
            data = fd.read()
            fd.close()
            (root, ext) = os.path.splitext(path)
            print ext, MIME_TYPE.get(ext, 'text/plain')
            response = Response(data, mimetype=MIME_TYPE.get(ext, 'text/plain'))
        else:
            response = Response('Error 404.', status=404)
    
    return response(environ, start_response)


#app = SteppingApp({})
run_simple('127.0.0.1', 5555, application, use_debugger=True, use_reloader=True)
