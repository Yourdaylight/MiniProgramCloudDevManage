# 微信云开发管理后台（开发中）
## 项目介绍
微信云开发使用的云数据库，云存储，云函数等都需要打开微信云开发者工具管理。
本项目基于uniapp + flsak + mongodb + mysql实现了一个可供多端管理的后台系统，方便开发者进行管理。

## 项目结构
```

├── utils
│   ├── __init__.py
│   ├── operate_cloud_db.py # 云数据库操作

├── views # 视图
│   ├── __init__.py
│   ├── app_management.py # app管理视图
│   ├── cloud_database.py # 云数据库视图
│   ├── cloud_function.py # 云函数视图
│   └── cloud_storage.py # 云存储视图


├── app.py # 项目启动文件
├── config.ini # 项目配置文件
├── models.py # 数据库模型
├── README.md
├── requirements.txt # 项目依赖
├── server_config.py # flask配置文件
```

## 功能介绍
- [] 用户登录
  支持默认账号密码登录，基于本地的config.ini配置文件直接登陆。    
  也可以界面输入项目的appid和appsecret进行登录。
- [] 云数据库管理
  获取用户存放的所有数据库表信息    
  支持对云数据库的增删改查操作。
- [] 云存储管理
    获取用户存放的所有云存储文件信息    
    支持对云存储的增删改查操作。
- [] 云函数管理
    获取用户存放的所有云函数信息    
    支持对云函数的增删改查操作。

## 项目运行

## 项目部署
初次安装依赖
```
pip install -r requirements.txt
```
运行项目
```
python app.py
```
## 项目截图
