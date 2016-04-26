# encoding=utf-8
import os, sys
import struct
from twisted.internet.protocol import Protocol
import logging
import ConTypes.procontypes as pts


class MstColProtocolException(Exception):
    pass


class MstColProtocol(Protocol):
    '''

    '''
    def __init__(self):
        '''
        :return:
        '''
        self._buffer = b''
        self._hostmetrics = {}
        self._epegmetrics = {}
        self._mqnmetrics = {}
        self._parse_status = 0

    def dataReceived(self, data):
        '''
        :param data:
        :return:
        '''

        self._buffer = self._buffer + data
        while True:
            if len(self._buffer) >= 4:
                length, = struct.unpack("<I", self._buffer[0, 4])
                if len(self._buffer) >= 4 + length:
                    self._parseBody(self._buffer[:length])


                else:
                    break
            else:
                break

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


    def _parseBody(self, hd):
        pk_len, pk_cmd, pk_seq = struct.unpack("<III", hd[:12])
        if not pk_cmd in pts:
            logging.error("cmd(%d) is unknow ", pk_cmd)
            return None

        if pk_cmd == pts.PROTO_NET_LOGIN_RESP:
            self.resp_rt = self._parseResp(hd[12: 16])
            return self.resp_rt
        elif pk_cmd == pts.PROTO_NET_ACTIVE_RES:
            pass
        elif pk_cmd == pts.PROTO_NET_IHOSTMETRICS_RESP:
            self._parseHostBody(hd[12: pk_len])
        else:
            pass

    def _parseResp(self, hd):
        resp_rt = struct.unpack("<I", hd)
        pass

    def _parseHostBody(self, host_buf):
        '''
        :param host_buf:
        :return:
        '''
        tmp_str = ''

        host_dict = {}
        host_dict['id'] = struct.unpack("<I", host_buf[:4])
        filedlist = host_buf[4:].split(str='\0', num=9)
        for idx, tmp_str in enumerate(filedlist):
            if idx == 0:
                host_dict['ip'] = tmp_str
            elif idx == 1:
                host_dict['name'] = tmp_str
            elif idx == 2:
                host_dict['os_name'] = tmp_str
            elif idx == 3:
                host_dict['os_release'] = tmp_str
            elif idx == 4:
                host_dict['machine_type'] = tmp_str
            elif idx == 5:
                host_dict['mount_type'] = tmp_str
            elif idx == 6:
                host_dict['cpu_desc'] = tmp_str
            elif idx == 7:
                host_dict['cpu_speed'] = tmp_str
            else:

                break

        (host_dict['cores_number'], host_dict['mem_total'], host_dict['swap_total'], host_dict['disk_total'],
         host_dict['cpu_idle_time'], host_dict['cpu_nice_time'], host_dict['cpu_sys_time'], host_dict['cpu_user_time'],
         host_dict['cpu_wio_time'], host_dict['mem_free'], host_dict['swap_free'], host_dict['mem_buffers'],
         host_dict['mem_cached'], host_dict['mem_shared'], host_dict['disk_free'], host_dict['timestamp'],
         host_dict['utimestamp']) = struct.unpack("<IIIQIIIIIIIIIIQII", tmp_str)

        self.self._hostmetrics = host_dict

    def _parseEpegBody(self, epeg_net_buf=None):
        '''
        :param self:
        :return:
        '''
        epeg_dict = {}
        if epeg_net_buf == None or len(epeg_net_buf) <= 0:
            logging.error("epeg buf is None! ", sys._getframe().f_code.co_name)
            raise MstColProtocolException, pts.PROTO_RESP_SUCCSS

        (epeg_dict['node_id'], epeg_dict['proc_total'], epeg_dict['proc_active'], epeg_dict['timestamp'],
         epeg_dict['utimestamp']) = struct.unpack("<IIIII", epeg_net_buf[:struct.calcsize("IIII")])

        p_num = epeg_dict['proc_active']
        p_len = struct.calcsize("IIII")

        while p_num > 0:
            p_dict = {}
            filedlist = epeg_net_buf[:].split(str='\0', num=3)
            for idx, tmp_str in enumerate(filedlist):
                if idx == 0:
                    p_dict['p_name'] = tmp_str
                elif idx == 1:
                    p_dict['job_name'] = tmp_str
                else:
                    pass

            (p_dict['idx'], p_dict['extern_idx'], p_dict['proc_status'],
             p_dict['proc_pid'], tmp_str) = struct.unpack("<BBBH%ds"%len(tmp_str)-struct.calcsize("BBBH"), tmp_str)

            p_dict['proc_version'], tmp_buf = tmp_str.split('\0', 2)

            (p_dict['proc_starttime'], p_dict['cpu'], p_dict['memory'], p_dict['flow_counts'], p_dict['status'],
             tmp_str) = struct.unpack("<IIIII%ds"%len(tmp_str)-struct.calcsize("IIIII"), tmp_str)

            q_num = p_dict['flow_counts']

            while q_num > 0:
                q_dict = {}
                q_dict['queue_name'], tmp_str = tmp_str.split('\0', 2)
                (q_dict['direction'], q_dict['emsgs'], q_dict['bytes']) = struct.unpack("<BQQ",
                                                                            tmp_str[:struct.calcsize("BQQ")])
                p_dict[q_dict['queue_name']] = q_dict
                q_num = int(q_num) - 1


            epeg_dict[p_dict['p_name']] = p_dict

        p_num = int(p_num) - 1

        self._epegmetrics = epeg_dict



    def _parseMqnBody(self, mqn_net_buf):
        '''
        :param self:
        :return:
        '''
        mqn_dict = {}
        if mqn_net_buf == None or len(mqn_net_buf) <= 0:
            logging.error("mqn buf is None! ", sys._getframe().f_code.co_name)
            raise MstColProtocolException, pts.PROTO_RESP_SUCCSS

        (mqn_dict['node_id'], mqn_dict['queue_total'], mqn_dict['queue_active'], mqn_dict['memcache_size'],
         mqn_dict['memcache_used'], mqn_dict['retrans_count'], mqn_dict['timestamp'],
         mqn_dict['utimestamp']) = struct.unpack("<IIIIIIIII", mqn_net_buf[:struct.calcsize("IIIIIIII")])

        q_num = mqn_dict['queue_active']
        q_len = struct.calcsize("IIII")

        queue_str = mqn_net_buf[struct.calcsize('IIIIIIII'):]
        while q_num > 0:
            q_dict = {}
            q_dict['queue_name'], queue_str = queue_str.split(str='\0', num=2)
            q_dict['queue_store'], queue_str = struct.unpack("<Q", queue_str[:struct.calcsize('Q')])
            mqn_dict[q_dict['queue_name']] = q_dict
            q_num = int(q_num) - 1

        self._mqnmetrics = mqn_dict



