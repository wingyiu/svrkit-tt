# -*- coding: utf-8 -*-

import time

from app.account.thf.ttypes import Account
from svrkit.service import BaseHandler


class AccountHandler(BaseHandler):
    def __init__(self):
        super(AccountHandler, self).__init__()

    def ping(self, seq_id, ball):
        print(ball)
        return ball

    def reg(self, seq_id, handle, password):
        t = int(time.time())
        account = Account(account_id=1, handle=handle, created_at=t, updated_at=t)
        return account

    def login(self, handle, password):
        pass

    def change_pwd(self, handle, password, new_password):
        pass
