from . import app
from flask import render_template, abort, redirect, url_for, session, g, make_response
from .forms import CompanySearchForm
import requests as req
import json
from .models import Company, db


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """
    """
    form = CompanySearchForm

    if form.validate_on_submit():
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data["symbol"] }/company')
        try:
            data = json.loads(res.text)
            company = {
                symbol = data[''],
                comapnyName= data[''],
                exchange= data[''],
                industry= data[''],
                website= data[''],
                description= data[''],
                CEO= data[''],
                issueType= data[''],
                sector= data[''],
            }
            new_company = Company(**company)
            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('.portfolio_detail'))
        except json.JSONDecodeError:
            abort(404)

    return render_template('search.html')
