# -*- coding: utf-8 -*-

import logging
from ConfigParser import ConfigParser
# import configparser

from thrift import TTornado
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from tornado import gen

logger = logging.getLogger(__name__)

class BaseClient(object):
    """
    read server list from configuration file
    use the `seq_id`
    """
    def __init__(self, client_cls, config_path):
        self.client_cls = client_cls
        # read configuration from ini file
        self.config_path = config_path
        self.parser = ConfigParser()
        self.parser.read(config_path)
        # only parse svrkit related configs
        configs = self._parse_configs(self.parser)
        self.servers = configs['servers']

    def _parse_configs(self, parser):
        configs = {}
        configs['service'] = {}
        configs['service']['name'] = parser.get('service', 'name')
        #if 'servers' in parser:
        configs['servers'] = []
        section_keys = parser.get('servers', 'keys').split(', ')
        for sk in section_keys:
            s = {}
            s['host'] = parser.get(sk, 'host')
            s['port'] = parser.getint(sk, 'port')
            configs['servers'].append(s)
        return configs

    def _get_server(self, seq_id):
        if seq_id is None:
            raise Exception('seq_id missing')
        logger.debug('seq_id: %s', seq_id)
        server_count = len(self.servers)
        idx = abs(hash(seq_id)) % server_count
        selected_server = self.servers[idx]
        logger.debug('selected server: [%d] %s:%s', idx, selected_server['host'], selected_server['port'])
        return selected_server

    @gen.coroutine
    def _remote_call(self, method, seq_id, *args, **kwargs):
        server = self._get_server(seq_id)
        # create client
        transport = TTornado.TTornadoStreamTransport(server['host'], server['port'])
        # open the transport, bail on error
        try:
            yield transport.open()
        except TTransport.TTransportException as ex:
            logging.error(ex)
            raise gen.Return()

        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        client = self.client_cls(transport, pfactory)

        # ping
        to_call = getattr(client, method)
        res = yield to_call(seq_id, *args, **kwargs)

        # close the transport
        client._transport.close()
        raise gen.Return(res)

    # @gen.coroutine
    # def __call__(self, method, *args, **kwargs):
    #     if 'seq_id' in kwargs:
    #         seq_id = kwargs.pop('seq_id')
    #     else:
    #         seq_id = args[0]
    #         args = args[1:]
    #     res = yield self._remote_call(method, seq_id, *args, **kwargs)
    #     raise gen.Return(res)
    #
    # def __getattr__(self, method):
    #     # 返回一个闭包,该闭包封装了self和method.
    #     # 当这个闭包被执行时,即x(*args, **kwargs),
    #     # 即self(method, *args, **kargs)被运行,
    #     # 即self.__call__(self, method, *args, **kwargs)
    #     f = lambda *args, **kwargs: self(method, *args, **kwargs)
    #     return f