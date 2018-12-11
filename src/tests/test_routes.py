from .. import app
import pytest


def test_home_route_get():
    rv = app.test_client.get('/')
    import pydb; pydb.start_trace()
    assert rv.status_code == 200
