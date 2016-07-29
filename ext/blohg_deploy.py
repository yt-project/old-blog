# -*- coding: utf-8 -*-

import os
import ipaddress
import hglib
from flask import request
from blohg.ext import BlohgBlueprint, BlohgExtension

ext = BlohgExtension(__name__)
deploy = BlohgBlueprint('deploy', __name__, url_prefix='/deploy')

BB_RANGE1 = ipaddress.ip_network(u'104.192.143.192/28', strict=False)
BB_RANGE2 = ipaddress.ip_network(u'104.192.143.208/28', strict=False)

@deploy.route('/', methods=['POST'])
def update_blog():
    addr = ipaddress.ip_address(unicode(request.headers.get('X-Real-IP')))
    if addr in BB_RANGE1 or addr in BB_RANGE2: 
        client = hglib.open(os.getcwd())
        updated = client.pull(update=True)
        client.close()
        return 'Repository updated: {}'.format(updated), 200
    else:
        return "Address {} is not authorized".format(str(addr)), 403


@ext.setup_extension
def setup_extension(app):
    app.register_blueprint(deploy)
