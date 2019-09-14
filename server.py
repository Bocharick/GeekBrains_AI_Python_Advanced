import yaml
from argparse import ArgumentParser
import os
import socket


if __name__ == "__main__":
    config = {
        'host': 'localhost',
        'port': 8000,
        'buffersize': 1024,
    }

    parser = ArgumentParser()

    parser.add_argument('-c', '--config', type=str, required=False, help="Sets config path")
    parser.add_argument('-ht', '--host', type=str, required=False, help='Sets server host')
    parser.add_argument('-p', '--port', type=str, required=False, help='Sets server port')

    args = parser.parse_args()

    if args.config:
        if os.path.isfile(args.config):
            with open(args.config) as file:
                file_config = yaml.safe_load(file)
                config.update(file_config or {})
        else:
            print(f'{args.config} is not a file')
            exit()

    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    while True:
        client, (client_host, client_port) = sock.accept()
        print(f'Client {client_host}:{client_port} was connected')

        bytes_request = client.recv(buffersize)
        print(f'Request: {bytes_request.decode()}')
        client.send(bytes_request)
        client.close()


