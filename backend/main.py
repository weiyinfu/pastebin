import flask
from flask import request, jsonify
import os
import json
import hashlib
import schedule
import threading
from typing import Dict
import sys

app = flask.Flask(__name__,static_folder="../front/dist", static_url_path="/")


def md5(s):
    m = hashlib.md5()
    m.update(bytes(s, encoding='utf8'))
    return m.hexdigest()


target_dir = os.path.join(os.path.expanduser("~"), 'log', 'pastebin')
assert os.path.exists(target_dir), f"{target_dir} not exists !"
"""
为了磁盘考虑，只保存最近使用过的文件，定期删除创建日期较早的文件
"""


@app.route("/api/get_file")
def get_file():
    filename = request.args['filename']
    filename = md5(filename)
    filepath = os.path.join(target_dir, filename)
    data = json.load(open(filepath, encoding='utf8'))
    return jsonify(data)


def validate(data: Dict):
    print(data)
    assert len(data) == 2
    assert 'filename' in data
    assert 'content' in data


@app.route("/api/put_file",methods=["POST"])
def put_file():
    # 上传文件
    content = request.get_data(as_text=True)
    if len(content) > 102400:
        return "文件太大"
    content = json.loads(content)
    validate(content)
    filename = content['filename']
    filename = md5(filename)
    filepath = os.path.join(target_dir, filename)
    json.dump(content, open(filepath, mode='w', encoding='utf8'))
    return "ok"


def clean():
    # 清除多余文件
    files = os.listdir(target_dir)
    pairs = []
    for file in files:
        filepath = os.path.join(target_dir, file)
        mtime = os.path.getmtime(filepath)
        pairs.append((filepath, mtime))
    pairs.sort(key=lambda x: x[1])
    while len(pairs) > 100:
        filepath, _ = pairs.pop()
        os.remove(filepath)


def worker():
    # 每周清理一次多余文件
    schedule.every(7).days.do(clean)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    threading.Thread(target=worker).start()
    app.run(debug=True,port=int(sys.argv[1]))
