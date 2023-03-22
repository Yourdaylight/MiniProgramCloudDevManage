# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:26
# @Author  :lzh
# @File    : server_config.py
# @Software: PyCharm
# database.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# 从config.ini中读取数据库配置
import os
import configparser
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
