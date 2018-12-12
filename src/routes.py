from flask import render_template, abort, redirect, url_for, request
from json import JSONDecodeError
from .models import db, Company
import requests as req
from . import app
from .forms import CompanySearchForm
import json
import requests


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """
    """
    form = CompanySearchForm()

    if form.validate_on_submit():
        symbol = form.data['symbol']
        res = requests.get(f'https://api.iextrading.com/1.0/stock/{ symbol }/company')


        data = json.loads(res.text)


        return redirect(url_for('.portfolio_detail'))

    return render_template('portfolio/search.html', form=form)


@app.route('/preview', methods=['GET', 'POST'])
def preview_company():
    """
    """

        # company = Company(
        #     symbol=data['symbol'],
        #     companyName=data['companyName'],
        #     exchange=data['exchange'],
        #     industry=data['industry'],
        #     website=data['website'],
        #     description=data['description'],
        #     CEO=data['CEO'],
        #     issueType=data['issueType'],
        #     sector=data['sector'],
        # )

        # db.session.add(company)
        # db.session.commit()


@app.route('/portfolio')
def portfolio_detail():
    """
    """
    companies = Company.query.all()
    return render_template('portfolio/portfolio.html', companies=companies)
