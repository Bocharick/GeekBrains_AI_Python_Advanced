import zlib
from functools import wraps
import logging


def compression_middleware(func):
    @wraps(func)
    def wrapper(raw_request, *args, **kwargs):
        bytes_request = zlib.decompress(raw_request)
        logging.debug("Request was decompressed")
        bytes_respone = func(bytes_request, *args, **kwargs)
        compressed_response = zlib.compress(bytes_respone)
        logging.debug("Response was compressed")
        return compressed_response
    return wrapper
