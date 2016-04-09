# -*- coding: utf-8 -*-

from thrift.TTornado import TTornadoServer
from thrift.protocol import TBinaryProtocol

class Server(TTornadoServer):

    def __init__(self, service, handler_cls):
        handler = handler_cls()
        processor = service.Processor(handler)
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        super(Server, self).__init__(processor, pfactory)