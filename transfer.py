#####传入参数########
# 密码
# 原钱包的key路径
# 源钱包的地址（一次只能填写一个）

# 目的钱包地址key文件路径（自定义钱包文件绝对路径，只能浏览并选择本地目录）

# 需要转移的热点地址或列表（多选和单选）

######返回参数#######
#显示源钱包账户下所有热点列表

#转移的热点名称和目的地钱包地址以及转移的结果


from app import Transfer
import subprocess
import wexpect, base64, uuid, json, os, logging
from database import db_session
from app import NewWallet


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='logFile.log', level=(logging.DEBUG), format=LOG_FORMAT)
walletArry = []

#实时获取钱包中的热点，无须存放数据库。因为可能会新增热点
def get_hotspots(wallet):
    try:
        hotspots_result = []
        tmp = subprocess.run("helium-wallet --format json hotspots list -a {}".format(wallet), stdout=subprocess.PIPE)
        for hts in json.loads(tmp.stdout):
            # 需要将使用过的新钱包和总创建的新钱包进行比较
            hotspots = hts["hotspots"]
            for hp in hotspots:
                hotspots_result.append(hp["address"])

    except Exception as e:
        logging.info("列出钱包的热点失败:{}".format(str(e)))
        return {"data":"","msg":"钱包{}获取热点失败".format(wallet),"status":1}
    else:
        logging.info("钱包:{}列出热点成功")
        return {"data":{"address":wallet,"hotspots":hotspots_result},"msg":"获取成功","status":0}


def CmdExec(password1,key_path,ho,new_wall,success,fail):
    try:
        logging.info("开始执行命令")
        child = wexpect.spawn('cmd.exe')
        child.expect('>')
        # 转移热点将之前钱包的热点转移到新创建的钱包
        child.sendline("helium-wallet --format json -f {}  hotspots transfer  {}  {} --commit".format(key_path, ho, new_wall))
        child.expect('Password:')
        child.sendline(password1)
        child.buffer = ''
        child.expect('>')
        consoleData = child.before
        resultJsonStr = '{' + consoleData.replace('\r\n', '').replace(' ', '').split('{')[1].split('}')[0] + '}'
        logging.info(resultJsonStr)
        resultJson = json.loads(resultJsonStr)
        logging.info(resultJson)
        child.sendline('exit')
        child.wait()
    except Exception as e:
        logging.error("执行转移热点失败:{}".format(str(e)))
        CommitDb(ho,new_wall,1)
        fail.append({"source": ho, "dest": new_wall, "status": 1})
    else:
        db_session.query(NewWallet).filter_by(address=new_wall).update({'status': 1})
        db_session.commit()
        CommitDb(ho,new_wall,0)
        logging.info("执行转移热点成功:{}".format(ho))
        success.append({"source": ho, "dest": new_wall})
    return success,fail


def CommitDb(ho,new_wall,status):
    transfer = Transfer(source_hotspots=ho, dest_wallet=new_wall, status=status)
    db_session.add(transfer)
    db_session.commit()

def transfer(password1,wallets,srckey_paths,hotspots,dest_file):
    #列出钱包的热点
    logging.info("开始转移热点")
    fail = []
    success = []
    free_wallets = []

    # 目的钱包地址key文件路径,不填以默认地址
    if not srckey_paths:
        wallets_path = "./config/transfers/"
        if not os.path.exists(wallets_path):
            os.mkdir(wallets_path)
    # 填的话就应这个源地址为主，不填的话以本次新建钱包为源地址
    if dest_file:
        fread = dest_file.read()
        fwe = str(fread, 'utf-8')
        free_wallets = fwe.split("\r\n")

    else:
        # 列出之前钱包的热点
        # 需要将使用过的新钱包和总创建的新钱包进行比较
        we = db_session.query(NewWallet).filter_by(status=0).all()
        for w in we:
            free_wallets.append(w.address)
    if len(free_wallets) == 0:
        logging.info("没有可用的新钱包，请先创建新钱包")
        return {"data":"","msg":"没有可用的新钱包，请先创建新钱包","status": 1}

    for ho,new_wall in zip(hotspots,free_wallets):
        ho = ho.strip()
        new_wall = new_wall.strip()
        logging.info("source_hostpots:{}".format(str(ho)))
        logging.info("dest_wallet:{}".format(str(new_wall)))


        key_path = srckey_paths + wallets + ".key"
        logging.info(key_path)
        logging.info("helium-wallet --format json -f {}  hotspots transfer  {}  {} --commit".format(key_path,ho,new_wall))
        success,fail = CmdExec(password1,key_path,ho,new_wall,success,fail)

    results = {"data": {"success": success, "fail": fail}, "msg": "转移成功:个,失败:{}个体".format(len(success), len(fail)), "status": 0}
    return results


