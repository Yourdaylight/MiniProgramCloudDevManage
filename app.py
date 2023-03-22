from flask import Flask
from server_config import app, db
from flask_sqlalchemy import SQLAlchemy
from views.cloud_function import cloud_function
from views.cloud_database import cloud_database
from views.cloud_storage import cloud_storage
from views.app_management import user_management

app.register_blueprint(cloud_function, url_prefix='/cloud-function')
app.register_blueprint(cloud_database, url_prefix='/cloud-database')
app.register_blueprint(cloud_storage, url_prefix='/cloud-storage')
app.register_blueprint(user_management, url_prefix='/user-management')


# @app.before_first_request
# def create_tables():
#     db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
