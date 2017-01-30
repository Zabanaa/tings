# Test Decorators that need a request

How do you test a decorator you use on your view functions without having to
make a request using the test client ?

just use

```python

# test.py
from app import app
from app.decorators import mydec

def fake_view_function():
    return jsonify({'key', 'value'})

class TestBase():

    def test_my_decorator():
        with app.test_request_context():
           decorated_view_function = mydec(fake_view_function)
           result = decorated_view_function()
           assert result.data == {'key': 'value'}
```

flask provides a test_request_context helper function. I use it to mock the
request object so that I don't have to create an http request.

make sure to give your decorated function another name otherwise it will raise
an exception 'local variable declared before assignement'
