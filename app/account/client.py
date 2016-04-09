# -*- coding: utf-8 -*-


import logging

from svrkit.client import BaseClient
from app.account.thf import AccountService

class AccountClient(BaseClient):

    def __init__(self, conf_path):
        super(AccountClient, self).__init__(AccountService.Client, conf_path)

