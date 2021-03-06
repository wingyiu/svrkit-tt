# -*- coding: utf-8 -*-

#
# Autogenerated by svrkit
#

import logging
from tornado import gen
from svrkit.client import BaseClient
from app.account.thf import AccountService
from app.account.thf import ttypes as account_ttypes
from app.account.thf import constants as account_constants


class AccountClient(BaseClient, AccountService.Iface):
    def __init__(self, conf_path):
        super(AccountClient, self).__init__(AccountService.Client, conf_path)
    
    @gen.coroutine
    def ping(self, seq_id, ball):
        """
        
        Parameters:
         - seq_id
         - ball
        
        """
        res = yield self._remote_call('ping', seq_id, ball)
        raise gen.Return(res)
    
    @gen.coroutine
    def change_pwd(self, seq_id, handle, password, new_password):
        """
        
        Parameters:
         - seq_id
         - handle
         - password
         - new_password
        
        """
        res = yield self._remote_call('change_pwd', seq_id, handle, password, new_password)
        raise gen.Return(res)
    
    @gen.coroutine
    def login(self, seq_id, handle, password):
        """
        
        Parameters:
         - seq_id
         - handle
         - password
        
        """
        res = yield self._remote_call('login', seq_id, handle, password)
        raise gen.Return(res)
    
    @gen.coroutine
    def reg(self, seq_id, handle, password):
        """
        
        Parameters:
         - seq_id
         - handle
         - password
        
        """
        res = yield self._remote_call('reg', seq_id, handle, password)
        raise gen.Return(res)
    