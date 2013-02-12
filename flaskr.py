from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create application
app = Flask(__name__)
app.config.from_object(__name__)


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


@app.route('/')
def show_entries():
    """
    Shows all entries from database
    """
    cur = g.db.execute(
        'SELECT title, text FROM entries ORDER BY id DESC'
    )
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute(
        'INSERT INTO entries (title, text) values (?, ?)',
        [request.form['title'], request.form('text')])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))




if __name__ == '__main__':
    app.run()
