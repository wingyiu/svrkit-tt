# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado import options
from svrkit.server import Server
from app.account.thf import AccountService
from app.account.service import AccountHandler


options.define("port", default=8080, help="run on the given port", type=int)

def main():
    options.parse_command_line()
    port = options.options.port
    server = Server(AccountService, AccountHandler)
    server.bind(port)
    server.start(1)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()