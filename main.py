import logging
import time

from flask import Flask, request
import json
import logging

from app import NewWallet, Transfer, BalancePay
from database import db_session
from flask_cors import CORS
from flask import render_template

#
app = Flask(__name__,
            static_folder="./static",
            static_url_path="",
            template_folder="./static")

CORS(app,resource='/*')
@app.route('/')
def index():
    return render_template("index.html")

from create_basic import create_main

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logFile.log', level=(logging.DEBUG), format=LOG_FORMAT)

def verfite(key,dicts):
    if key not in dicts.keys():
        return True



# 数量
# 密码
# KEY文件保存的路径
@app.route('/api/basics', methods=["POST"])
def create_basic():

    # 加个判断是否存在数据，不存在则直接返回错误
    print("213123")
    if verfite("password",request.get_json()):
        return {"data":"","msg":"缺少参数:{}".format("password"),"status":1}
    if verfite("count",request.get_json()):
        return {"data":"","msg":"缺少参数:{}".format("count"),"status":1}
    password1 = request.get_json()["password"]
    count = request.get_json()["count"]
    paths = request.get_json()["paths"]
    print(paths,password1,count)
    #create_result = create_main(password1, int(count), paths)
    return json.dumps({"data":{},"msg":"获取成功","status":0})


# 获取所有创建的新钱包以及是否使用状态
@app.route('/api/basics', methods=["GET"])
def get_basic():
    querys = db_session.query(NewWallet).all()
    results = []
    for n in querys:
        results.append({"id": n.id, "address": n.address})
    return json.dumps({"data":results,"msg":"获取成功","status":0})


# 显示源钱包账户下所有热点列表
from transfer import get_hotspots
@app.route('/api/transfer', methods=["GET"])
def get_hotspot():
    wallet = request.args.get("wallet")
    print(wallet)
    time.sleep(4)
   #results = get_hotspots(wallet)
    return json.dumps({"data":{"address":wallet,"hotspots":["dads","dadsasd"]},"msg":"获取成功","status":0})


from transfer import transfer


@app.route('/api/transfer', methods=["POST"])
def tranfers():

    password1 = request.form.get("password")
    hotspots = request.form.get("hotspots").split(",")
    wallets = request.form.get("wallets")
    srckey_paths = request.form.get("srckey_paths")
    logging.info("transfer")
    if request.form.get("file"):
        dest_file = ""

    else:
        dest_file = request.files['file']

    logging.info(dest_file)
    logging.info(password1)
    logging.info(hotspots)
    logging.info(wallets)
    results = transfer(password1, wallets, srckey_paths, hotspots,dest_file)
    return json.dumps(results)


# @app.route('/api/transfer', methods=["GET"])
# def get_tranfer():
#     querys = db_session.query(Transfer).all()
#     results = []
#     for t in querys:
#         results.append(
#             {"id": t.id, "source_hotspots": t.source_hotspots, "dest_wallet": t.dest_wallet, "status": t.status})
#     return json.dumps(results)


#
#
from balance_pay import banlance_pay
#
#
@app.route('/api/balance_pay', methods=["POST"])
def balance_pay():
    if verfite("wallets",request.get_json()):
        return {"data":"","msg":"缺少参数:{}".format("wallets"),"status":1}

    if verfite("password",request.get_json()):
        return {"data":"","msg":"缺少参数:{}".format("password"),"status":1}

    wallet = request.get_json()["wallets"]
    addressPwd = request.get_json()["password"]
    paths = request.get_json()["srckey_paths"] #源钱包的key文件路径
    results = banlance_pay(wallet, addressPwd, paths)
    return results



@app.route('/api/balance_pay', methods=["GET"])
def get_balance():
    querys = db_session.query(BalancePay).all()
    results = []
    for ba in querys:
        results.append(
            {"id": ba.id, "source_wallet": ba.source_wallet, "dest_wallet": ba.dest_wallet, "status": ba.status,
             "blance": ba.blance})
    return json.dumps({"data":results,"msg":"获取成功","status":0})



if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
