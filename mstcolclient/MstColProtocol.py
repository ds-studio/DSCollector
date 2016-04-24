# encoding=utf-8

from struct import pack, unpack
from twisted.internet.protocol import Protocol




class MstColProtocol(Protocol):
    def __init__(self):
        self._buffer = b''

    def dataReceived(self, data):
        self._buffer = self._buffer + data
        while True:
            if len(self._buffer) >= 4:
                length, = unpack("<I", self._buffer[0, 4])
                if len(self._buffer) >= 4 + length:
                    header_data = self._buffer[4: 12]
                    self.parseHeader(header_data)

                else:
                    break
            else:
                break


        handlePackageHeader(data)
        pass

    def dataSend(self):
        pass

    def connectionMade(self):
        pass

    def makeConnection(self, transport):
        pass

    def connectionLost(self):
        pass


    def _buildHeader(self):
        pass

    def _buildHostBody(self):
        pass

    def _buildEpegBody(self):
        pass

    def _buildMqnBody(self):
        pass


    def _parseHeader(self, hd):
        pass

    def _parseBody(self, hd):
        pass

    def _parseHostBody(self):
        pass

    def _parseEpegBody(self):
        pass

    def _parseMqnBody(self):
        pass




