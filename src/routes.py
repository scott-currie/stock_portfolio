from . import app
from flask import render_template, abort, redirect, url_for, session, g, make_response


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')
