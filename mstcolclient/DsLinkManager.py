# encoding=utf-8

from twisted.internet.protocol import ClientFactory
from twisted.internet.defer import Deferred
from DsColProtocol import MstColProtocol
import DsUtils
import logging


class DsLinkInfo(object):
    '''
    :function descript
    link base data
    '''

    def __init__(self, server_ip, server_port, rec_time, req_time):
        self._ip = server_ip
        self._port = server_port
        self._rec_time = rec_time
        self._req_time = req_time
        self._send = 0

    def mstcolconnect(self):
        pass


class DsLinkManager(object):
    def __init__(self, cl_server):
        self._node_table = {}
        self._node_count = 0
        self._step = self._node_count

    def addSvcNode(self, addr, DsLinkElem):
        addr = DsUtils.check_address(addr)
        if not addr and not addr in self._node_table:
            self._node_table.pop(addr, DsLinkElem)
        else:
            logging.error("addr(%s) is invaid!" % addr)
            return None

        return addr

    def delSvcNode(self, addr):
        if addr in self.node_table.keys():
            self._node_table.__delitem__(addr)
        else:
            logging.error("addr(%s) is not exist!" % addr)
            return None

        return addr

    def next(self):
        return self._node_table.next(self)

    def __iter__(self):
        return self

    def linkDisploy(self):
        print self


