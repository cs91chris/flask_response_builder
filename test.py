import pytest

from datetime import datetime

from flask import json
from flask import Flask
from flask import abort
from flask import Response as Resp

from flask.testing import FlaskClient
from werkzeug.utils import cached_property

from flask_response_builder import ResponseBuilder


@pytest.fixture
def app():
    class Response(Resp):
        @cached_property
        def json(self):
            return json.loads(self.data)

    class TestClient(FlaskClient):
        def open(self, *args, **kwargs):
            if 'json' in kwargs:
                kwargs['data'] = json.dumps(kwargs.pop('json'))
                kwargs['Content-Type'] = 'application/json'
            return super(TestClient, self).open(*args, **kwargs)

    _app = Flask(__name__)
    _app.config['RB_HTML_DEFAULT_TEMPLATE'] = 'response.html'
    rb = ResponseBuilder(_app)

    data = {
        "users": [
            {
                "id": 1,
                "name": "Leanne Graham",
                "email": "Sincere@april.biz",
                "phone": "1-770-736-8031 x56442",
                "sysdate": datetime.now(),
                "address": {
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {"lat": -37.3159, "lon": 81.1496}
                },
                "test": [
                    {"a": 1, "b": 2},
                    {"a": 2, "b": 3},
                ]
            },
            {
                "id": 2,
                "name": "Ervin Howell",
                "email": "Shanna@melissa.tv",
                "phone": "010-692-6593 x09125",
                "sysdate": datetime.now(),
                "address": {
                    "city": "Wisokyburgh",
                    "zipcode": "90566-7771",
                    "geo": {"lat": -43.9509, "lon": -34.4618}
                },
                "test": [
                    {"a": None, "b": None}
                ]
            }
        ]
    }

    @_app.route('/<path:fmt>')
    def index(fmt):
        if fmt == 'json':
            return rb.json(data)
        if fmt == 'xml':
            return rb.xml(data)
        if fmt == 'yaml':
            return rb.yaml(data)
        if fmt == 'html':
            return rb.html(data['users'], name='Users', as_table=True)
        if fmt == 'csv':
            return rb.csv(data['users'], filename='users')
        if fmt == 'base64':
            return rb.base64(data)
        else:
            abort(400)

    @_app.route('/nocontent')
    @ResponseBuilder.no_content
    def nocontent():
        pass

    @_app.route('/xhr')
    @rb.template_or_json('response.html')
    def test_xhr():
        return data['users']

    @_app.route('/onaccept')
    @rb.on_accept()
    def test_accept():
        return data['users']

    @_app.route('/onacceptonly')
    @rb.on_accept(acceptable=['application/xml'])
    def test_acceptonly():
        return data['users']

    @_app.route('/customaccept')
    def test_customaccept():
        _, builder = rb.get_mimetype_accept()
        return rb.build_response(builder, data['users'])

    @_app.route('/format')
    @rb.on_format()
    def test_format():
        return data['users']

    @_app.route('/decorator')
    @rb.response('json')
    def test_decorator():
        resp = data['users'][0]
        resp.pop('sysdate')
        return resp, 206, {'header': 'header'}

    _app.response_class = Response
    _app.test_client_class = TestClient
    _app.testing = True
    return _app


@pytest.fixture
def client(app):
    _client = app.test_client()
    return _client


def test_app_runs(client):
    res = client.get('/')
    assert res.status_code == 404


def test_app_returns_correct_content_type(client):
    res = client.get('/html')
    assert res.status_code == 200
    assert 'text/html' in res.headers['Content-Type']

    res = client.get('/json')
    assert res.status_code == 200
    assert 'application/json' in res.headers['Content-Type']

    res = client.get('/xml')
    assert res.status_code == 200
    assert 'application/xml' in res.headers['Content-Type']

    res = client.get('/yaml')
    assert res.status_code == 200
    assert 'application/yaml' in res.headers['Content-Type']

    res = client.get('/csv')
    assert res.status_code == 200
    assert 'text/csv' in res.headers['Content-Type']

    res = client.get('/base64')
    assert res.status_code == 200
    assert 'application/base64' in res.headers['Content-Type']


def test_no_content(client):
    res = client.get('/nocontent')
    assert res.status_code == 204
    assert res.headers.get('Content-Length') in (None, 0)


def test_on_format(client):
    res = client.get('/format?format=xml')
    assert res.status_code == 200
    assert 'application/xml' in res.headers['Content-Type']

    res = client.get('/format?format=yaml')
    assert res.status_code == 200
    assert 'application/yaml' in res.headers['Content-Type']

    res = client.get('/format')
    assert res.status_code == 200
    assert 'application/json' in res.headers['Content-Type']


def test_on_accept(client):
    res = client.get('/onaccept', headers={'Accept': '*/*'})
    assert res.status_code == 200
    assert 'application/json' in res.headers['Content-Type']

    res = client.get('/onaccept', headers={'Accept': 'application/xml'})
    assert res.status_code == 200
    assert 'application/xml' in res.headers['Content-Type']

    res = client.get('/onaccept', headers={'Accept': 'text/csv'})
    assert res.status_code == 200
    assert 'text/csv' in res.headers['Content-Type']

    res = client.get('/onaccept', headers={'Accept': 'custom/format'})
    assert res.status_code == 406


def test_on_accept_only(client):
    res = client.get('/onacceptonly', headers={'Accept': 'application/xml'})
    assert res.status_code == 200
    assert 'application/xml' in res.headers['Content-Type']

    res = client.get('/onacceptonly', headers={'Accept': 'application/json'})
    assert res.status_code == 406


def test_custom_accept(client):
    res = client.get('/customaccept', headers={'Accept': 'application/xml'})
    assert res.status_code == 200
    assert 'application/xml' in res.headers['Content-Type']


def test_template_or_json(client):
    res = client.get('/xhr')
    assert res.status_code == 200
    assert 'application/json' in res.headers['Content-Type']

    res = client.get('/xhr', headers={'X-Requested-With': 'XMLHttpRequest'})
    assert res.status_code == 200
    assert 'text/html' in res.headers['Content-Type']


def test_response_decorator(client):
    res = client.get('/decorator')
    assert res.status_code == 206
    assert 'application/json' in res.headers['Content-Type']
    assert res.headers['header'] == 'header'
