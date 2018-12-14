from flask import render_template, abort, redirect, url_for, request, session, flash, g
# from json import JSONDecodeError
from .models import db, Company, Portfolio, User
# import requests as req
from . import app
from .forms import CompanySearchForm, CompanyAddForm, PortfolioAddForm
import json
import requests
from sqlalchemy.exc import DBAPIError, IntegrityError, InvalidRequestError
import functools
from .auth import login_required


@app.add_template_global
def get_portfolios():
    return Portfolio.query.all()


@app.route('/')
def home():
    """Handle GET requests on the home route.

    return: render the home page
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def company_search():
    """ Handle GET or POST methods on company search route.
    POSTs from CompanySearchForm are passed through the remote API,
    and data returned is converted to JSON. This data becomes session
    context for creating Company objects elsewhere.

    returns: redirect to company preview on POST
    returns: render search page on GET
    """
    form = CompanySearchForm()

    # This path represents a POST
    if form.validate_on_submit():
        symbol = form.data['symbol']
        res = requests.get(f'https://api.iextrading.com/1.0/stock/{ symbol }/company')

        data = json.loads(res.text)
        session['context'] = data
        return redirect(url_for('.company_preview'))
    # This is a GET
    return render_template('portfolio/search.html', form=form)


@app.route('/company', methods=['GET', 'POST'])
@login_required
def company_preview():
    """Handle GET and POST on company preview route. Bundle up the session
    context and populate it with data from session['context']. On POSTs,
    try to instantiate a Company from the form data.

    return: render search page and CompanyAddForm if add fails
    return: redirect to portfolio details route if add success
    return:
    """
    form_context = {
        'symbol': session['context']['symbol'],
        'companyName': session['context']['companyName'],
        'exchange': session['context']['exchange'],
        'industry': session['context']['industry'],
        'website': session['context']['website'],
        'description': session['context']['description'],
        'CEO': session['context']['CEO'],
        'issueType': session['context']['issueType'],
        'sector': session['context']['sector']
    }
    form = CompanyAddForm(**form_context)
    if form.validate_on_submit():
        try:
            company = Company(
                symbol=form.data['symbol'],
                portfolio_id=form.data['portfolios'],
                companyName=form.data['companyName'],
                exchange=form.data['exchange'],
                industry=form.data['industry'],
                website=form.data['website'],
                description=form.data['description'],
                CEO=form.data['CEO'],
                issueType=form.data['issueType'],
                sector=form.data['sector'],
            )
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError, InvalidRequestError):
            abort(404)
            flash('An error occurred trying to add this company.')
            # Error in writing to db. End this req/res cycle and render search page.
            return render_template('portfolio/search.html', form=form)
        # Write was successful. Redirect to portfolio detail page
        print('Successful write to database.')
        return redirect(url_for('.portfolio_detail'))
    # This was a POST method. Render the portfolio preview with form context
    return render_template('portfolio/preview.html', form=form, company_data=session['context'])


@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio_detail():
    """Handle GET and POST on portfolio route. On POST, use name from
    form data to create a new Portfolio.

    return: render seach page if portfolio add fails
    return: return redirect to search page if portfolio add success
    return: return render portfolio if this is a GET
    """

    form = PortfolioAddForm()

    if form.validate_on_submit():
        try:
            portfolio = Portfolio(name=form.data['name'], user_id=g.user.id)
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('There was a problem creating your portfolio.')
            return render_template('portfolio/search.html', form=form)
        # Create portfolio was successful. Redirect to search.html
        return redirect(url_for('.company_search'))

    # import pdb; pdb.set_trace()
    user_portfolios = Portfolio.query.filter(
        Portfolio.user_id == g.user.id).all()
    portfolio_ids = [p.id for p in user_portfolios]

    return render_template('portfolio/portfolio.html', form=form)
