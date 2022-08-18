######传入参数#######
# 数量
# 密码
# KEY文件保存的路径
######返回参数#######
# address（分页功能）和创建结果


import json
from posixpath import split
import time, sys
from unittest import result
import configparser
from apps import NewWallet
from multiprocessing import Pool, cpu_count
import os
import time
from database import db_session
import wexpect, base64, uuid, json, os, logging


def get_a_uuid():
    r_uuid = str(uuid.uuid1())
    return r_uuid.replace('=', '')


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logFile.log', level=(logging.DEBUG), format=LOG_FORMAT)



def creates(password1, paths):
    logging.info("开始创建新钱包")
    if not paths:
        paths = './dataKeys/'
        if not os.path.exists(paths):
            os.mkdir(paths)
    try:
        fileNameId = get_a_uuid()
        logging.info("创建命令是:{}".format('helium-wallet --format json  create basic --output  ' + paths + fileNameId + '.key'))
        resultJson = cmdexec(password1,paths,fileNameId)
    except Exception as e:
        logging.error("创建错误原因:{}".format(str(e)))
        return True
    else:
        logging.info("创建成功")
        newallet = NewWallet(address=resultJson['address'],status=0)
        db_session.add(newallet)
        db_session.commit()
        return False


def cmdexec(password1,paths,fileNameId):
    logging.info("开始执行命令")
    print('23423222222')
    cmd_string = "cmd.exe"
    child = wexpect.spawn(cmd_string)
    child.expect('>')
    child.sendline('helium-wallet --format json  create basic --output  ' + paths + fileNameId + '.key')
    child.expect('Password:')
    child.sendline(str(password1))
    child.expect('Confirm password:')
    child.sendline(str(password1))
    child.buffer = ''
    child.expect('>')
    consoleData = child.before
    resultJsonStr = '{' + consoleData.replace('\r\n', '').replace(' ', '').split('{')[1].split('}')[0] + '}'
    logging.info(resultJsonStr)
    resultJson = json.loads(resultJsonStr)
    keyFileName = resultJson['address'] + '.key'
    os.rename(paths + fileNameId + '.key', paths + keyFileName)
    resultJson['keyFileName'] = keyFileName
    child.logfile = sys.stdout
    child.sendline('exit')
    child.wait()
    return  resultJson



def create_main(password1, count, paths):
    logging.info('当前母进程: {}'.format(os.getpid()))
    p = Pool(6)
    fails = []
    success = []
    for i in range(count):
        ws = p.apply_async(creates, args=(password1, paths))
        reslt = ws.get()
        if reslt:
            success.append('1')
        else:
            fails.append('0')
    results = {"data":"","msg":"创建成功个数:{},失败个数:{}".format(len(success),len(fails)),"status":1} # 返回创建成功和失败的结果
    p.close()
    p.join()
    return results
