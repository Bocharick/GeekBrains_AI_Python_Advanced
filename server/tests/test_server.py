from datetime import datetime
from protocol import make_response, make_200, make_400, make_404, make_500, validate_request
from resolvers import find_server_action
import pytest


@pytest.fixture
def expected_code():
    return 200


@pytest.fixture
def expected_action():
    return 'test'


@pytest.fixture
def expected_time():
    return datetime.now().timestamp()


@pytest.fixture
def expected_data():
    return 'some client data'


@pytest.fixture
def initial_request(expected_action, expected_time, expected_data):
    return {
        "action": expected_action,
        "time": expected_time,
        "data": expected_data
    }


@pytest.fixture
def expected_response(expected_action, expected_time, expected_data, expected_code):
    return {
        "action": expected_action,
        "time": expected_time,
        "data": expected_data,
        "code": expected_code
    }


@pytest.fixture
def code_200():
    return 200


@pytest.fixture
def code_400():
    return 400


@pytest.fixture
def code_404():
    return 404


@pytest.fixture
def code_500():
    return 500


@pytest.fixture
def valid_request():
    return {
        'action': 'test',
        'time': datetime.now().timestamp(),
        'data': 'some test data'
    }


@pytest.fixture
def invalid_request():
    return {
        'data': 'some test data'
    }


def test_make_respone(initial_request, expected_response, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    assert response == expected_response


def test_action_make_response(initial_request, expected_action, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    action = response.get('action')
    assert action == expected_action


def test_code_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    code = response.get('code')
    assert code == expected_code


def test_time_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    time = response.get('time')
    assert time == expected_time


def test_data_make_response(initial_request, expected_code, expected_data, expected_time):
    response = make_response(initial_request, expected_code, expected_data, expected_time)
    data = response.get('data')
    assert data == expected_data


def test_none_request_make_response(expected_code):
    with pytest.raises(AttributeError):
        response = make_response(None, expected_code)


def test_make_response_200(initial_request, expected_data, expected_time, code_200):
    response = make_200(initial_request, expected_data, expected_time)
    code = response.get('code')
    assert code == code_200


def test_make_response_400(initial_request, expected_data, expected_time, code_400):
    response = make_400(initial_request, expected_data, expected_time)
    code = response.get('code')
    assert code == code_400


def test_make_response_404(initial_request, expected_time, code_404):
    response = make_404(initial_request, expected_time)
    code = response.get('code')
    assert code == code_404


def test_make_response_500(initial_request, expected_time, code_500):
    response = make_500(initial_request, expected_time)
    code = response.get('code')
    assert code == code_500


def test_valid_validate_request(valid_request):
    response = validate_request(valid_request)
    assert response


def test_invalid_validate_request(invalid_request):
    response = validate_request(invalid_request)
    assert response == False


def test_find_server_action():
    server_actions = find_server_action()
    assert type(server_actions) is dict
