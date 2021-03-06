# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Gennady Denisov.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from flask.views import View
from flask import render_template


class BaseView(View):
    """
    Base view
    """
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)


class ListView(BaseView):
    """
    Base view for showing list of entries
    """
    def dispatch_request(self):
        context = {'objects': self.get_objects()}
        return self.render_template(context)


class FormView(BaseView):
    methods = ['GET', 'POST']




