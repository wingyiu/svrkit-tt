# -*- coding: utf-8 -*-
import os
import sys
from tornado import gen
from tornado import ioloop

from app.account.client import AccountClient, account_ttypes, account_constants

@gen.coroutine
def test():
    conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client.ini')
    client = AccountClient(conf_path)
    res = yield client.ping(1, 'o')
    print(res)

    handle = account_ttypes.AccountHandle(username='wingyiu')
    try:
        res = yield client.reg(1, handle, '123456')
    except:
        print(sys.exc_info()[0])
    print(res)
    raise gen.Return()


def main():
    # create an ioloop, do the above, then stop
    ioloop.IOLoop.current().run_sync(test)


if __name__ == "__main__":
    main()