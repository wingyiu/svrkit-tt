# -*- coding: utf-8 -*-

from thrift import TTornado
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from tornado import gen
from tornado import ioloop

from app.account.client import AccountClient

@gen.coroutine
def test():
    client = AccountClient('/Users/user/Git/svrkit-tt/app/account/test/client.ini')
    for i in range(100):
        bk = yield client.ping(i, str(i))
        print(bk)
    raise gen.Return()


def main():
    # create an ioloop, do the above, then stop
    ioloop.IOLoop.current().run_sync(test)


if __name__ == "__main__":
    main()