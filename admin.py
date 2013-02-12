# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Gennady Denisov.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.


from flask.ext.admin import BaseView, expose
from flask import url_for


# Admin views
class MyView(BaseView):
    @expose('/')
    def index(self):
        # Get URL for the test view method
        url = url_for('.test')
        return self.render('admin/index.html', url=url)

    @expose('/test/')
    def test(self):
        return self.render('admin/test.html')


