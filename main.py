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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from AttributeSet import AttributeSet
from FD import FD
from FDset import FDset

class MainHandler(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, {}))

class ResultHandler(webapp.RequestHandler):
  def post(self):
    F = FDset()
    fds = self.request.get('fds').strip('{}').split(',')
    for fd in fds:
      left,right = fd.split('->')
      #right = fd.split('->')[1]
      F.add(FD(AttributeSet(left),AttributeSet(right)))
    G = F.LMinimumSet()
    path = os.path.join(os.path.dirname(__file__), 'result.html')
    self.response.out.write(template.render(path, {'originalset':F, 'lminimumset':G}))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/result', ResultHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
