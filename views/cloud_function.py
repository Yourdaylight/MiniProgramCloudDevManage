# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:34
# @Author  :lzh
# @File    : cloud_function.py
# @Software: PyCharm
# modules/cloud_function.py
from flask import Blueprint

cloud_function = Blueprint('cloud_function', __name__)


@cloud_function.route('/cloud-function')
def index():
    return "Cloud Function Management"
