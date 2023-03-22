# -*- coding: utf-8 -*-
# @Time    :2022/7/9 15:27
# @Author  :lzh
# @File    : operate_cloud_db.py
# @Software: PyCharm
import os
import time
import json
import requests, random, string
from requests_toolbelt import MultipartEncoder


def get_access_token(appid, appsecret):
    """"
    获取access_token
    """
    with open("token.json", "r") as f:
        config = json.loads(f.read())
    now_time = int(time.time())
    # access_token两小时有效，超时则重新请求获取
    if now_time - config.get("update_time", 0) >= 7200:
        wechart_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}'
        response = requests.get(wechart_url)
        result = response.json()
        config = {
            "token": result["access_token"],
            "update_time": now_time
        }
        with open("token.json", "w") as f:
            f.write(json.dumps(config))

    return config["token"]  # 将返回值解析获取access_token


class Cloud:
    def __init__(self, appid, appsecret, env, collection_name):
        self.access_token = get_access_token(appid, appsecret)
        self.query_url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={self.access_token}'
        self.add_url = f'https://api.weixin.qq.com/tcb/databaseadd?access_token={self.access_token}'
        self.update_url = f'https://api.weixin.qq.com/tcb/databaseupdate?access_token={self.access_token}'
        self.delete_url = f'https://api.weixin.qq.com/tcb/databasedelete?access_token={self.access_token}'
        self.upload_url = f'https://api.weixin.qq.com/tcb/uploadfile?access_token={self.access_token}'
        self.download_url = f'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token={self.access_token}'
        self.cloud_function_url = f'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token={self.access_token}'
        self.env = env
        self.collection_name = collection_name
        self.post_data = {"env": self.env}  # 请求参数，每次的请求参数需要env环境id和query查询语句

    def query(self, search_param, fields=None):
        """
        search_param: dict
        """
        if fields is None:
            fields = {}
        self.post_data["query"] = f"db.collection('{self.collection_name}').where({search_param}).field({json.dumps(fields)}).limit(100).get()"
        res = requests.post(self.query_url, data=json.dumps(self.post_data))
        return res.json()

    def update(self, search_param, update_dict):
        """
        search_param:dict 查询要更新的某条记录
        update_dict:dict 要修改的值
        """
        update_data = "{data:%s}" % update_dict
        self.post_data["query"] = f"db.collection('{self.collection_name}').where({search_param}).update({update_data})"
        response = requests.post(self.update_url, data=json.dumps(self.post_data))
        result = response.json()
        return result

    def add(self, new_data):
        """
        new_data: list of dict
        """
        new_data = "{data:%s}" % new_data
        self.post_data["query"] = f"db.collection('{self.collection_name}').add({new_data})"
        response = requests.post(self.add_url, data=json.dumps(self.post_data))
        result = response.json()
        # 执行成功返回状态码0
        if result["errcode"] == 0:
            return result['id_list']
        else:
            return result

    def delete(self, search_param):
        self.post_data["query"] = f"db.collection('{self.collection_name}').where({search_param}).remove()"
        res = requests.post(self.delete_url, data=json.dumps(self.post_data))
        return res.json()

    def upload(self, file_name):
        post_data = {"env": self.env, "path": file_name}
        res = requests.post(self.upload_url, data=json.dumps(post_data))
        return res.json()

    def download(self, file_id, max_age=7200):
        post_data = {"env": self.env, "file_list": [{"fileid": file_id, "max_age": max_age}]}
        res = requests.post(self.download_url, data=json.dumps(post_data))
        return res.json()

    def invoke_cloud_function(self, function_name, post_data):
        res = requests.post(self.cloud_function_url,
                            data={"env": self.env, "name": function_name, "req_data": json.dumps(post_data)})
        return res.json()


def upload_file(_cloud, filename, cloud_dir_name="./"):
    """
    _cloud:(Cloud) Cloud对象
    filename(str) 本地文件路径
    cloud_dir_name(str) 云端文件夹路径
    """
    # 第一次请求获取上传连接
    upload_path = f"{cloud_dir_name}/{filename}"
    res = cloud.upload(upload_path)
    file_id = res['file_id']
    # 从上传链接中获取file_id检查该文件是否存在
    check_exisit = _cloud.download(file_id)
    # 调用下载链接确认文件不存在再上传
    if check_exisit["errcode"] == 0 and check_exisit["file_list"][0]["status"] == 1:
        # 拿到上传连接后获取密钥，读取本地文件流上传
        if res["errcode"] == 0:
            post_data = {
                "key": upload_path,
                "Signature": res["authorization"],
                "x-cos-security-token": res["token"],
                "x-cos-meta-fileid": res["cos_file_id"],
                "file": open(filename, "rb")
            }
            url = res["url"]
            body = MultipartEncoder(
                fields=post_data,
                boundary=''.join(random.sample(string.ascii_letters + string.digits, 30))
            )
            headers = {"Content-Type": body.content_type}
            upload_res = requests.post(url, data=body, headers=headers)
            if upload_res.status_code != 204:
                print(upload_res.content)
                import sys
                sys.exit(0)

    else:
        print(f"{cloud_dir_name}文件已存在,直接读取")


if __name__ == '__main__':
    # 从config.ini的[cloud]中读取appid和appsecret
    import configparser
    config = configparser.ConfigParser()
    config.read("../config.ini")
    appid = config.get("app", "appid")
    appsecret = config.get("app", "appsecret")
    env = config.get("app", "env")
    collection_name = "user"
    print(appid, appsecret, env, collection_name)
    # 新建一个Cloud对象
    cloud = Cloud(appid, appsecret, env, collection_name)
    # 查询
    search_param = {"_openid": "oQKgO5Q0f9dX0X1qX1qX1qX1qX1q"}
    fields = {"_id": 1, "name": 1, "age": 1}
    result = cloud.query(search_param, fields)
