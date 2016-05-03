# encoding=utf-8

from collections import deque
from twisted.internet.defer import Deferred
from twisted.protocols.basic import LineReceiver
from  twisted.internet import protocol, reactor



class simpleClientProtocol(LineReceiver):
    delimiter = '\n'

    def __init__(self, factory):
        self._current = deque() # 用于存放sendCmd中返回的deferred对象， 以便数据返回时可以处理
        self._factory = factory

    def connectionMade(self):
        self._factory._deferred.callback(self)

    def connectionLost(self, reason):
        #如果该连接在连接池中，则从池中删除， 否则释放该连接，以唤醒等待队列
        try:
            self._factory.pool._pool.remove(self)
        except:
            self._factory.pool.release(None)

    def get(self):
        return self.sendCmd('get', 'get %s' % key)

    def sendCmd(self, cmd, fullcmd):
        cmdObj = Command(cmd, fullcmd)
        #防止在连串操作过程中连接丢失
        if not self.transport.connected:
            cmdObj._deferred.errback(-1)
            return cmdObj._deferred
        self._current.append(cmdObj)
        self.sendLine(fullcmd)
        self.transport.doWrite()
        return cmdObj._deferred

    def lineReceived(self, data):
        cmd = self._current.popleft()
        cmd.success(data, self)


class simpleClientFactory(protocol.ClientFactory):
    def __init__(self, simple_client_pool, d):
        self._deferred = d #传入一个deferr对象用于回调
        self.pool = simple_client_pool

    def buildProtocol(self, addr):
        return simpleClientProtocol(self) #将自身传递给protocol

    def clientConnectionFailed(self, connector, reason):
        self.pool.release(None)
        self._deferred.errback(reason)




class Command(object):
    def __init__(self):
        self._deferred = Deferred()

    def success(self, value, client): #这里可以对返回结果做判断，决定是callback还是errback
        self._deferred.callback(value)

    def err(self, error):
        self._deferred.errback(error)


class simple_client_pool_t(object):
    def __init__(self, host, port, capacity):
        self._host = host
        self._port = port
        self._capacity = capacity
        self._in_use = 0
        self._pool = []
        self._waitlist = deque()

    def create_simple_client(self, deferred):
        simple_client_factory = simpleClientFactory(self, deferred)
        reactor.connectTCP(self._host, self._port, simple_client_factory)

    def aquire(self, deferred=None): #从等待队列过来的会自行带deferred
        if not deferred:
            deferred = Deferred()

        if self._pool:
            simple_client = self._pool.pop()
            self._in_use += 1
            deferred.callback(simple_client)
        elif self._in_use < self._capacity:
            self._in_use += 1
            self.create_simple_client(deferred)
        else:
            self._waitlist.append(deferred)

        return deferred

    def release(self, simple_client):
        if not simple_client: #释放的client已经失效
            self._in_use -= 1
            if self._waitlist:
                self.aquire(self._waitlist.popleft())
            return
        if self._waitlist: #等待队列不为空， 唤醒第一个等待
            self._waitlist.popleft().callback(simple_client)
        else:
            self._pool.append(simple_client)
            self._in_use -= 1


def get(key):
    def acquire_suc(client, key):
         client.get(key).addCallback(get_suc, key).addErrback(acquire_err)
    def acquire_err(result):
        deferred.errback(result) #deferred对象自动访问到外部的deferred， 变量作用域可查看这里

    def get_suc(value):
        deferred.errback(value)

    deferred = Deferred()
    client_pool.aquire().addCallback(acquire_suc, key).addErrback(acquire_err)
    return deferred

client_pool = simple_client_pool_t('127.0.0.1', 8000, 10)
get('key').addCallback(get_suc).addErrback(get_err)




