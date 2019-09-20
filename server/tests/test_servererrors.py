from datetime import datetime
from servererrors.controllers import errors_controller
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


def test_errors_controller():
    with pytest.raises(Exception) as e:
        response = errors_controller(REQUEST)
    assert str(e.value) == "Server error"
