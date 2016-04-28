# -*- coding: utf-8 -*-
import sys
import time
import logging
import hashlib
import functools
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from app.account.thf.ttypes import *
from app.account.thf import AccountService
from svrkit.handler import BaseHandler
from app.account.model import AccountModel
from app.account import settings


def with_session(method):
    @functools.wraps(method)
    def wrapped(*args, **kw):
        try:
            ret = method(*args, **kw)
            # args[0] = self
            args[0].session.commit()
            return ret
        except:
            args[0].session.rollback()
            raise

    return wrapped


class AccountHandler(BaseHandler, AccountService.Iface):
    def __init__(self):
        super(AccountHandler, self).__init__()
        # &use_unicode=0 return str
        db_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8&use_unicode=0' % (settings.DATABASES['USER'],
                                                                                settings.DATABASES['PASSWORD'],
                                                                                settings.DATABASES['HOST'],
                                                                                settings.DATABASES['PORT'],
                                                                                settings.DATABASES['NAME'])
        db_engine = create_engine(db_url, convert_unicode=False, pool_recycle=7200, pool_size=1, max_overflow=2,
                                  echo=False,
                                  echo_pool=False)

        DbSession = sessionmaker(bind=db_engine)
        AccountModel.metadata.create_all(bind=db_engine)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.WARN)
        self.session = DbSession()

    def ping(self, seq_id, ball):
        logging.info('seq_id: %d', seq_id)
        return ball

    def __encrypt_password(self, plain, salt):
        return hashlib.sha1((plain + salt).encode('utf-8')).hexdigest()

    def __gen_salt(self):
        return hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()

    @with_session
    def reg(self, seq_id, handle, password):
        logging.info('seq_id: %d', seq_id)
        # 新建account model
        model = AccountModel()
        model.username = handle.username
        model.phone = handle.phone
        model.email = handle.email
        model.salt = self.__gen_salt()
        model.password = self.__encrypt_password(password, salt=model.salt)
        model.status = 0

        try:
            self.session.add(model)
            self.session.commit()
        except IntegrityError as e:
            raise AccountExisted('handle duplicated')
        except:
            logging.exception(sys.exc_info()[0])
            raise Exception('exception happen')
        account = Account(account_id=model.account_id,
                          username=model.username,
                          phone=model.phone,
                          email=model.email,
                          status=model.status,
                          created_at=model.created_at,
                          updated_at=model.updated_at)
        return account

    def login(self, seq_id, handle, password):
        pass

    def change_pwd(self, seq_id, handle, password, new_password):
        pass
