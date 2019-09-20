from datetime import datetime
from protocol import make_response, make_200, make_400, make_404, make_500, validate_request
from resolvers import find_server_action
import pytest

CODE = 200
ACTION = 'test'
TIME = datetime.now().timestamp()
DATA = 'some client data'
REQUEST = {
    "action": "test",
    "time": TIME,
    "data": DATA
}
RESPONSE = {
    "data": DATA,
    "code": CODE,
    "action": "test",
    "time": TIME
}


def test_make_respone():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    assert response == RESPONSE


def test_action_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    action = response.get('action')
    assert action == ACTION


def test_code_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    code = response.get('code')
    assert code == CODE


def test_time_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    time = response.get('time')
    assert time == TIME


def test_data_make_response():
    response = make_response(REQUEST, CODE, DATA, date=TIME)
    data = response.get('data')
    assert data == DATA


def test_none_request_make_response():
    with pytest.raises(AttributeError):
        response = make_response(None, CODE)


def test_make_respone_200():
    response = make_200(REQUEST, DATA, TIME)
    assert response == RESPONSE


def test_make_respone_400():
    response = make_400(REQUEST, DATA, TIME)
    code = response.get('code')
    assert code == 400


def test_make_respone_404():
    response = make_404(REQUEST, TIME)
    code = response.get('code')
    assert code == 404


def test_make_respone_500():
    response = make_500(REQUEST, TIME)
    code = response.get('code')
    assert code == 500


def test_validate_request():
    response = validate_request(REQUEST)
    assert response


def test_find_server_action():
    server_actions = find_server_action()
    assert type(server_actions) is dict