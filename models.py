# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:21
# @Author  :lzh
# @File    : models.py
# @Software: PyCharm
# models.py
from server_config import db


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.String(64), index=True, unique=True)
    appsecret = db.Column(db.String(64), index=True, unique=True)
    env = db.Column(db.String(64), index=True, unique=True)
    program_name = db.Column(db.String(64), index=True)
    access_token = db.Column(db.String(64), index=True)
    # 最近更新时间的时间戳
    update_time = db.Column(db.Integer)

    def __repr__(self):
        return f'<Appid {self.appid}>'
