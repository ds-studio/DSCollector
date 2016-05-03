# encoding=utf-8
import logging


def check_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            logging.error('Ports must be integers.')
            return None

        return addr