# -*- coding: utf-8 -*-

import os
import ipaddress
import hglib
from flask import request
from blohg.ext import BlohgBlueprint, BlohgExtension

ext = BlohgExtension(__name__)
deploy = BlohgBlueprint('deploy', __name__, url_prefix='/deploy')

BB_RANGE1 = ipaddress.ip_network(u'131.103.20.160/24', strict=False)
BB_RANGE2 = ipaddress.ip_network(u'165.254.145.0/26', strict=False)
BB_RANGE3 = ipaddress.ip_network(u'104.192.143.0/24', strict=False)


@deploy.route('/', methods=['POST'])
def update_blog():
    addr = ipaddress.ip_address(unicode(request.headers.get('X-Real-IP')))
    if addr in BB_RANGE1 or addr in BB_RANGE2 or addr in BB_RANGE3:
        client = hglib.open(os.getcwd())
        updated = client.pull(update=True)
        client.close()
        return 'Repository updated: {}'.format(updated), 200
    else:
        return "Address {} is not authorized".format(str(addr)), 403


@ext.setup_extension
def setup_extension(app):
    app.register_blueprint(deploy)
