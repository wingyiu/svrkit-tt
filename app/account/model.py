# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.sql import func
from svrkit.model import BaseModel


class AccountModel(BaseModel):
    """账号模型"""
    __tablename__ = 'account'
    # ID
    account_id = Column(Integer, primary_key=True)
    # 用户名
    handle = Column(String(50), unique=True)
    # 手机号
    phone = Column(CHAR(11), unique=True)
    # 邮箱
    email = Column(String(255), unique=True)
    # 加密后的密码
    password = Column(String(40))
    # 随机盐
    salt = Column(String(32))
    # 上次登录
    last_login = Column(Integer)
    # 状态 (0正常,1禁用)
    status = Column(Integer, default=0)
    # 注册时间
    created_at = Column(Integer, default=func.unix_timestamp())
    # 更新时间
    updated_at = Column(Integer, default=func.unix_timestamp(), onupdate=func.unix_timestamp())
