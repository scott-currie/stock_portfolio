from .. import app
import pytest


def test_home_route_get():
    rv = app.test_client().get('/')
    assert rv.status_code == 200

def test_portfolio_route_get():
    rv = app.test_client().get('/search')
    assert rv.status_code == 200

def test_portfolio_route_post():
    rv = app.test_client().post('/search', data={'symbol': 'MSFT'})
    assert rv.status_code == 302
