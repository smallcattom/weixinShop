# -*- coding:utf-8 -*-
import sae
from weixin import app
application = sae.create_wsgi_app(app)