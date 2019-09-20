from datetime import datetime
from servertime.controllers import timestamp_controller
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


def test_timestamp_controller():
    response = timestamp_controller(REQUEST)
    time = response.get('time')
    assert type(time) is float
