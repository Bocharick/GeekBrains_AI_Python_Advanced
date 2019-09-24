import yaml
import json
import socket
import select
import logging
from argparse import ArgumentParser
from resolvers import find_server_action
from protocol import validate_request, make_200, make_500, make_400, make_404
from handlers import handle_tcp_request

config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024,
}

parser = ArgumentParser()
parser.add_argument('-c', '--config', type=str, required=False,
                    help='Sets config path')
parser.add_argument('-ht', '--host', type=str, required=False,
                    help='Sets server host')
parser.add_argument('-p', '--port', type=str, required=False,
                    help='Sets server port')

args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        file_config = yaml.safe_load(file)
        config.update(file_config or {})

host = args.host if args.host else config.get('host')
port = args.port if args.port else config.get('port')
buffersize = config.get('buffersize')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)

requests = []
connections = []

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    # sock.setblocking(False)
    # В винде sock.setblocking(False) скорее всего не работает, и можно его заменить командой sock.settimeout(1)
    sock.settimeout(1)
    sock.listen(5)

    logging.info(f'Server started with {host}:{port}')

    action_mapping = find_server_action()

    while True:
        try:
            client, (client_host, client_port) = sock.accept()
            logging.info(f'Client {client_host}:{client_port} was connected')
            connections.append(client)
        except Exception as e:
            pass

        if connections:
            rlist, wlist, xlist = select.select(
                connections, connections, connections, 0
            )

            for read_client in rlist:
                bytes_request = client.recv(buffersize)
                requests.append(bytes_request)

            if requests:
                bytes_request = requests.pop()
                bytes_response = handle_tcp_request(bytes_request, action_mapping)

                for write_client in wlist:
                    write_client.send(bytes_response)

except KeyboardInterrupt:
    logging.info('Server shutdown')
