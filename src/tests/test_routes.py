from .. import app
from .. models import db
import pytest


@pytest.fixture
def client():
    def do_nothing():
        pass
    db.session.commit = do_nothing
    yield app.test_client()
    db.session.rollback()


def test_home_route_get_returns_200():
    """Check the status code of a get on / is 200."""
    rv = app.test_client().get('/')
    assert rv.status_code == 200


def test_home_route_get_returns_html():
    """Check the data returned by a get on / has expected content."""
    rv = app.test_client().get('/')
    assert b'<h1>Welcome to the site</h1>' in rv.data


def test_portfolio_route_get_returns_200():
    """Check the status code of a get on /search is 200."""
    rv = app.test_client().get('/search')
    assert rv.status_code == 200


def test_portfolio_route_post_returns_302(client):
    """Check that a post method with valid input data on /search returns status code 302."""
    rv = client.post('/search', data={'symbol': 'MSFT'})
    assert rv.status_code == 302

