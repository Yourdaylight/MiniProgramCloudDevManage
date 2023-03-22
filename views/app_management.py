# -*- coding: utf-8 -*-
# @Time    :2023/3/22 7:35
# @Author  :lzh
# @File    : user_management.py
# @Software: PyCharm

# modules/user_management.py
from flask import Blueprint

user_management = Blueprint('user_management', __name__)


@user_management.route('/user-management')
def index():
    return "User Management"
