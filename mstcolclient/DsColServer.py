# encoding=utf-8
from DsLinkManager import DsLinkPool
from twisted.internet.defer import Deferred
from DsColProtocol import DsColFactory
import DsUtils
import logging

def DataSave(resq_data):
    '''
    :func:
        data is saved into zookeeper node ,  if host nodes is limited,  clean the
        oldest one.
    :param resq_data:
    :return:
    '''
    print resq_data

class CollectService(object):

    poem = None # the cached poem

    def __init__(self, addr, type):
        ip, port = DsUtils.check_address(addr)
        if ip is None or port is None:
            logging.error("ip %s or port %d is invaid!!" % ip, port)
        self._ip = ip
        self._port = port
        self._nodetype = type

    def get_collect_data(self):
        def canceler(d):
            print 'Canceling link download.'
            factory.deferred = None
            connector.disconnect()

        print 'Fetching poem from server.'
        deferred = Deferred(canceler)
        deferred.addCallback(self.set_poem)
        factory = DsColFactory(deferred, type)
        from twisted.internet import reactor
        connector = reactor.connectTCP(self.host, self.port, factory)
        return factory.deferred

    def set_poem(self, poem):
        self.poem = poem
        return poem
