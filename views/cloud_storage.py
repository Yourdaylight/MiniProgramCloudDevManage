# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:34
# @Author  :lzh
# @File    : cloud_storage.py
# @Software: PyCharm
# modules/cloud_storage.py
from flask import Blueprint

cloud_storage = Blueprint('cloud_storage', __name__)


@cloud_storage.route('/cloud-storage')
def index():
    return "Cloud Storage Management"
