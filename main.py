#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import os
import wsgiref.handlers

#from google.appengine.ext import webapp
#from google.appengine.ext.webapp import template
import jinja2
import webapp2

from AttributeSet import AttributeSet
from FD import FD
from FDset import FDset

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.out.write(template.render())
    #path = os.path.join(os.path.dirname(__file__), 'index.html')
    #self.response.out.write(template.render(path, {}))

class ResultHandler(webapp2.RequestHandler):
  def post(self):
    if self.request.get('fds'):
      F = FDset()
      fds = self.request.get('fds').strip('{}').split(',')
      for fd in fds:
        left,right = fd.split('->')
        F.add(FD(AttributeSet(left),AttributeSet(right)))
      G = F.LMinimumSet()
      #path = os.path.join(os.path.dirname(__file__), 'result.html')
      template_values = {'originalset':F, 'lminimumset':G}
      template = JINJA_ENVIRONMENT.get_template('result.html')
      self.response.out.write(template.render(template_values))
    else:
      logging.error("IP adress %s attempted to access ResultHandler without sending fds data."%self.request.remote_addr)
      self.redirect("/")

app = webapp2.WSGIApplication([('/', MainHandler),('/result', ResultHandler)])

#def main():
#  application = webapp.WSGIApplication([('/', MainHandler),
#                                        ('/result', ResultHandler)],
#                                       debug=True)
#  wsgiref.handlers.CGIHandler().run(application)
#
#if __name__ == '__main__':
#  main()
#
