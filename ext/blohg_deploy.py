# -*- coding: utf-8 -*-

import os
import hglib
from blohg.ext import BlohgBlueprint, BlohgExtension

ext = BlohgExtension(__name__)
deploy = BlohgBlueprint('deploy', __name__, url_prefix='/deploy')


@deploy.route('/')
def update_blog():
    client = hglib.open(os.getcwd())
    updated = client.pull(update=True)
    client.close()
    return 'Repository updated: {}'.format(updated)


@ext.setup_extension
def setup_extension(app):
    app.register_blueprint(deploy)
