import hashlib
import json
import os
import threading
from typing import Dict

import flask
import schedule
from flask import request, jsonify

static_folder = os.path.join(os.path.dirname(__file__), "../front/dist/")
assert os.path.exists(static_folder)
app = flask.Flask(__name__, static_url_path="/", static_folder=static_folder,)


def md5(s):
    m = hashlib.md5()
    m.update(bytes(s, encoding="utf8"))
    return m.hexdigest()


target_dir = os.path.join(os.path.expanduser("~"), "log", "pastebin")
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
assert os.path.exists(target_dir), f"{target_dir} not exists !"
"""
为了磁盘考虑，只保存最近使用过的文件，定期删除创建日期较早的文件
"""


@app.route("/api/get_file")
def get_file():
    filename = request.args["filename"]
    filename = md5(filename)
    filepath = os.path.join(target_dir, filename)
    data = json.load(open(filepath, encoding="utf8"))
    return jsonify(data)


def validate(data: Dict):
    print(data)
    assert len(data) == 2
    assert "filename" in data
    assert "content" in data


@app.route("/api/put_file", methods=["POST"])
def put_file():
    # 上传文件
    content = request.get_data(as_text=True)
    if len(content) > 102400:
        return "文件太大"
    content = json.loads(content)
    validate(content)
    filename = content["filename"]
    filename = md5(filename)
    filepath = os.path.join(target_dir, filename)
    json.dump(content, open(filepath, mode="w", encoding="utf8"))
    return "ok"


@app.route("/")
def haha():
    return "hello world"


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


app.before_first_request = lambda: threading.Thread(
    target=worker
).start()  # 为了让gunicorn能够监控删除线程，此处把线程放在外面
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
