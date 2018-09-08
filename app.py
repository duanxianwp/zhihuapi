from flask import Flask, request

from db import MongoTools

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add_collect_task', methods=['POST'])
def add_collect_task():
    token = request.form['name']
    if MongoTools.insert_collect_task(token):
        return 'SUCCESS'
    else:
        return 'ERROR'


@app.route('/get_task_status', methods=['GET'])
def get_task_status():
    token = request.args.get('token')
    return MongoTools.get_task_status(token)


if __name__ == '__main__':
    app.run(port=8080)
