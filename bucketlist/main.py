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
import webapp2
import os
import jinja2
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BucketList(ndb.Model):
    db_entry = ndb.StringProperty(required=True)
    db_date = ndb.DateTimeProperty(required=True)
    ID = ndb.StringProperty(required=True)

class CompletedList(ndb.Model):
    db_entry = ndb.StringProperty(required=True)
    db_date = ndb.DateTimeProperty(required=True)
    ID = ndb.StringProperty(required=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            q = ndb.gql("SELECT * FROM BucketList WHERE ID = :1", user.user_id())
            BucketList = q.get()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render())
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('about-us.html')
        self.response.write(template.render())
        user = users.get_current_user()
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class NewHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('new-adventure.html')
            self.response.write(template.render())
        else:
            template = JINJA_ENVIRONMENT.get_template('log-in.html')
            self.response.write(template.render())
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class BucketListSaver(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            entry = self.request.get('entry_in_form')
            db_bucket_list = BucketList(ID=users.get_current_user().user_id(), db_entry=entry, db_date=datetime.now())
            db_bucket_list.put()
            template = JINJA_ENVIRONMENT.get_template('thanks.html')
            self.response.write(template.render())
        else:
            template = JINJA_ENVIRONMENT.get_template('log-in.html')
            self.response.write(template.render())
        user = users.get_current_user()
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class CurrentHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            list_query = BucketList.query(BucketList.ID == users.get_current_user().user_id())
            list_query = list_query.order(BucketList.db_date)
            list_data = list_query.fetch()
            template = JINJA_ENVIRONMENT.get_template('current-list.html')
            self.response.write(template.render({'entries' : list_data}))
        else:
            template = JINJA_ENVIRONMENT.get_template('log-in.html')
            self.response.write(template.render())
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)

    def post(self):
        print 'delete is ' + self.request.get('delete')
        print 'move is ' + self.request.get('move')

        key_values = self.request.get('key', allow_multiple=True)
        for key in key_values:
            post_key = ndb.Key(urlsafe=key)
            result = post_key.get()
            post_key.delete()
            if self.request.get('move') == 'Completed!':
                db_completed_list = CompletedList(db_entry=result.db_entry, db_date=datetime.now(), ID=result.ID)
                db_completed_list.put()
        return self.get()
        user = users.get_current_user()
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)


class CompletedHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            list_query = CompletedList.query(CompletedList.ID == users.get_current_user().user_id())
            list_query = list_query.order(CompletedList.db_date)
            list_data = list_query.fetch()
            template = JINJA_ENVIRONMENT.get_template('completed-list.html')
            self.response.write(template.render({'entries' : list_data}))
        else:
            template = JINJA_ENVIRONMENT.get_template('log-in.html')
            self.response.write(template.render())
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)

class DiscoverHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('discover.html')
        self.response.write(template.render())
        user = users.get_current_user()
        if user:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign out</a>' %
                        (users.create_logout_url('/')))
        else:
            greeting = ('<a id="greeting" class="buttons" href="%s">Sign in or register</a>' %
                        users.create_login_url('/'))
        self.response.out.write('<html><body>%s</body></html>' % greeting)


app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/about-us', AboutHandler), ('/new-adventure', NewHandler),
    ('/current-list', CurrentHandler), ('/completed-list', CompletedHandler),
    ('/discover', DiscoverHandler), ('/save', BucketListSaver)

], debug=True)
