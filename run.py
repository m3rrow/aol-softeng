#!/usr/bin/env python3
import sys

def startFlask(host, port):
    from backend import app
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    # Set to false to hide debug log info
    app.config['DEBUG'] = True
    log.debug("[+] Listening on port {}".format(port))
    app.run(host=host, port=port)

if __name__ == '__main__':
    try:
        port = 8080
        host = "0.0.0.0"
        startFlask(host, port)
    except Exception as E:
        print(str(E))
        exit(1)