import yaml
import sys
from argparse import ArgumentParser
import os
import socket
import json




def make_request(text):
    return {
        "data": text
    }




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
    sock.connect((host, port))

    message = input('Enter your message: ')
    request = make_request(message)
    string_request = json.dumps(request)

    sock.send(string_request.encode())
    bytes_response = sock.recv(buffersize)

    response = json.loads(bytes_response)

    print(response)