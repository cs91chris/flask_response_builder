from flask import Flask
from flask import abort

from flask_response_builder import created_response
from flask_response_builder import no_content_response
from flask_response_builder import FlaskResponseBuilder


app = Flask(__name__)
app.config['RB_HTML_DEFAULT_TEMPLATE'] = 'response.html'
rb = FlaskResponseBuilder(app)


data = {
    "users": [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "phone": "1-770-736-8031 x56442",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            }
        },
        {
            "id": 2,
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv",
            "phone": "010-692-6593 x09125",
            "address": {
                "street": "Victor Plains",
                "suite": "Suite 879",
                "city": "Wisokyburgh",
                "zipcode": "90566-7771",
                "geo": {
                    "lat": "-43.9509",
                    "lng": "-34.4618"
                }
            }
        }
    ]
}


@app.route('/<path:fmt>')
def index(fmt):
    if fmt == 'json':
        return rb.json(data)
    if fmt == 'xml':
        return rb.xml(data)
    if fmt == 'yaml':
        return rb.yaml(data)
    if fmt == 'html':
        return rb.html(data['users'], name='Users')
    if fmt == 'csv':
        return rb.csv(data['users'], 'users')
    if fmt == 'base64':
        return rb.base64(data)
    else:
        abort(404)


@app.route('/nocontent')
@no_content_response
def nocontent():
    pass


@app.route('/created')
@created_response
def created():
    return {'message': 'created'}, {'link': '/linkme'}


@app.route('/testxhr')
@rb.template_or_json('response.html')
def test_xhr():
    return data['users']


@app.route('/accept')
@rb.on_accept()
def test_accept():
    return data['users']


@app.route('/format')
@rb.on_format()
def test_format():
    return data['users']


@app.route('/decorator')
@rb.response('csv', filename='test')
def test_decorator():
    return data['users']


if __name__ == '__main__':
    app.run()
