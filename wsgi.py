#!/usr/bin/env python

try:
    import os, sys
    os.chdir(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath(os.curdir))
    from setup import * #@UnusedWildImport
    from os import environ
    from django.core.handlers.wsgi import WSGIHandler
    environ.update(DJANGO_SETTINGS_MODULE='settings')
    application = WSGIHandler()
except:
    print >> sys.stderr, sys.exc_info()[1]

if __name__ == '__main__':
    print >> sys.stderr, "in main"
    from werkzeug.debug import DebuggedApplication
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, DebuggedApplication(application, evalex=True), use_reloader=False, use_debugger=False)