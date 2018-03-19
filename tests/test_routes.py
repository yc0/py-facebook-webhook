import sys
import os
sys.path.append( os.path.join( os.path.dirname(__file__), os.path.pardir ) )
print(sys.path)
import __main__
import app


def test_webhook_routes_get():
    request, response = app.app.test_client.get('/webhook')
    assert response.text == 'Hello world'

    request, response = app.app.test_client.post('/webhook')
    print(request)
    print(response)
    assert response.status == 500
