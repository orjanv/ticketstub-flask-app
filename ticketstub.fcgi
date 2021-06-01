#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from stub import app

if __name__ == '__main__':
  WSGIServer(app, bindAddress = '/tmp/ticketstub-fcgi.sock').run()
