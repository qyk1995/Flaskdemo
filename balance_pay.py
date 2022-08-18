###########传入参数##########
# 密码
# 指定源钱包KEY文件路径（默认为创建新钱包时的默认目录）
# 目的钱包地址（每次只能填写一个地址）

#######返回参数#########
# 转移的源钱包地址和转移金额以及转移状态
# 本次转移的总金额


#data: 返回实际数据  msg: 报错信息 status 运行状态

import json
import wexpect, base64, uuid, json, os
import subprocess
import logging
from apps import NewWallet,BalancePay
from database import db_session

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logFile.log', level=(logging.DEBUG), format=LOG_FORMAT)


def cmd_exec(addressPwd,key_path,wallet,dest_wallet,balanc):
    child = wexpect.spawn('cmd.exe')
    child.sendline('helium-wallet --format json -f {}{}.key  pay one  {}  {} --commit'.format(key_path,wallet,dest_wallet,float(balanc)))
    child.expect('Password:')
    child.sendline(addressPwd)
    child.buffer = ''
    child.expect('>')
    consoleData = child.before
    resultJsonStr = consoleData.replace('\r\n', '').replace(' ', '')
    jsonstr = resultJsonStr.split(']')[1] + "]}"
    jsons = json.loads(jsonstr)
    amount = jsons["payments"][0]["amount"]
    logging.info(resultJsonStr)
    child.sendline('exit')
    child.wait()
    return amount


def CommitDb(wallet,dest_wallet,balanc,status):
    balan = BalancePay(source_wallet=wallet, dest_wallet=dest_wallet, blance=float(balanc), status=status)
    db_session.add(balan)
    db_session.commit()

def banlance_pay(dest_wallet, addressPwd,paths):
    logging.info("开始转账")
    used_wallets = []
    balans = []
    success = []
    fail = []
    # 已经转移过热点的新钱包才能进行转移金额
    if paths:
        key_path = paths
        for file in os.listdir(paths):
            address = file.split(".")[0]
            used_wallets.append(address)
    else:
        key_path = "./dataKey/"
        wes = db_session.query(NewWallet).filter_by(status=1).all()
        for wallet in wes:
            used_wallets.append(wallet.address)

    for wallet in used_wallets:
        # 查询余额
        wallet = wallet.strip()
        tmp = subprocess.run('helium-wallet --format json balance -a {}'.format(wallet), stdout=subprocess.PIPE,encoding='utf-8')
        balanc = json.loads(tmp.stdout)[0]['balance']
        adress = json.loads(tmp.stdout)[0]['address']
        logging.info('钱包名称:{},钱包金额: {}'.format(adress, balanc))
        try:
            #   判断账户余额是否满足 转账需求
            if float(balanc) - 0.040 > 0:
                logging.info('开始转账')
                balanc = float(balanc) - 0.040
                logging.info('helium-wallet --format json -f {}{}.key  pay one  {}  {} --commit'.format(key_path,wallet,dest_wallet,float(balanc)))
                logging.info("本次转账金额:{}".format(balanc))
                logging.info('钱包名称:{},钱包金额: {}'.format(adress, balanc))

                amount = cmd_exec(addressPwd,key_path,wallet,dest_wallet,balanc)
                # 计算amount 总额
                balans.append(float(amount))

            else:
                balan_data = '钱包:{}金额不足'.format(json.loads(tmp.stdout)[0]['address'])
                logging.info(balan_data)
                CommitDb(wallet, dest_wallet, balanc, 1)
                fail.append({"source_wallet":wallet,"dest_wallet":dest_wallet,"wallet":float(balanc),"message":"钱包金额不足"})
                continue
        except Exception as e:
            errdata = '钱包:{}转账失败'.format(json.loads(tmp.stdout)[0]['address'])
            logging.error(errdata)
            CommitDb(wallet, dest_wallet, balanc, 1)
            fail.append({"source_wallet":wallet,"dest_wallet":dest_wallet,"wallet":float(balanc),"message":"转移失败"})
        else:
            CommitDb(wallet, dest_wallet, balanc, 0)
            success.append({"source_wallet":wallet,"dest_wallet":dest_wallet,"wallet":float(balanc),"message":"转移成功"})

    result = {"data":{"success": success, "fail": fail,"total":sum(balans)},"msg": "转移成功:{}个,失败:{}个".format(len(success),len(fail)),"status": 0}

    return result



