# -*- coding: utf-8 -*-

import time
import logging

from app.account.thf.ttypes import *
from app.account.thf import AccountService
from svrkit.handler import BaseHandler
from app.account.model import AccountModel


class AccountHandler(BaseHandler, AccountService.Iface):
    def __init__(self):
        super(AccountHandler, self).__init__()

    def ping(self, seq_id, ball):
        logging.info('seq_id: %d', seq_id)
        return ball

    def reg(self, seq_id, handle, password):
        logging.info('seq_id: %d', seq_id)
        t = int(time.time())
        # 新建account model
        model = AccountModel()
        model.handle = handle
        model.password = password
        model.salt = xxx
        model.status = 0

        account = Account(account_id=1, handle=handle, created_at=t, updated_at=t)
        return account

    def login(self, seq_id, handle, password):
        pass

    def change_pwd(self, seq_id, handle, password, new_password):
        pass
