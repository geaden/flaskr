from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

from flask.views import MethodView, View
from views import ListView
from flask.ext.admin import Admin
from admin import MyView

# create application
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# connect to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


class EntriesListView(ListView):
    def get_template_name(self):
        return 'show_entries.html'

    def get_objects(self):
        cur = g.db.execute(
            'SELECT title, text FROM entries ORDER BY id DESC'
        )
        return [dict(title=row[0], text=row[1]) for row in cur.fetchall()]


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute(
        'INSERT INTO entries (title, text) values (?, ?)',
        [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash("You were logged in")
            return redirect(url_for('show_entries'))
    return  render_template('login.html', error=error)


class LogoutView(MethodView):
    def get(self):
        session.pop('logged_in', None)
        flash("You were logged out")
        return redirect(url_for('show_entries'))


app.add_url_rule(
    '/',
    view_func=EntriesListView.as_view('show_entries')
)
app.add_url_rule(
    '/logout',
    view_func=LogoutView.as_view('logout')
)

admin = Admin(app)

admin.add_view(MyView(name="Hello"))
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))

if __name__ == '__main__':
    init_db()
    app.run()
