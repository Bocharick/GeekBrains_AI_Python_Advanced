import logging
import json
from protocol import validate_request, make_200, make_500, make_400, make_404
from middlewares import compression_middleware

@compression_middleware
def handle_tcp_request(bytes_request, action_mapping):
    request = json.loads(bytes_request)
    if validate_request(request):
        action = request.get('action')
        controller = action_mapping.get(action)
        if controller:
            try:
                response = controller(request)
                # print(f'Request: {bytes_request.decode()}')
                logging.debug(f'Request: {bytes_request.decode()}')
            except Exception as err:
                response = make_500(request)
                # print(err)
                logging.critical(err)
        else:
            response = make_404(request)
            logging.error(f'Action with name {action} not found')
    else:
        response = make_404(request, 'Request is not valid')
        # print(f'Wrong request: {request}')
        logging.error(f'Wrong request: {request}')

    return json.dumps(response).encode()



