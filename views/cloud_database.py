# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:35
# @Author  :lzh
# @File    : cloud_database.py
# @Software: PyCharm
# modules/cloud_database.py
from flask import Blueprint
import models
cloud_database = Blueprint('cloud_database', __name__)

@cloud_database.route('/cloud-database')
def index():
    return "Cloud Database Management"
