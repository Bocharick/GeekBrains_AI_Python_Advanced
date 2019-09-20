from datetime import datetime
from echo.controllers import echo_controller
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


def test_echo_controller():
    response = echo_controller(REQUEST)
    assert response == RESPONSE
