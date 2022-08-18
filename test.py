######传入参数#######
# 数量
# 密码
# KEY文件保存的路径
######返回参数#######
# address（分页功能）和创建结果
import json


import os
import sys
from multiprocessing import Pool
from apps import NewWallet
from database import db_session

newallet = NewWallet(address="2e2qq7979eww", status=0)
db_session.add(newallet)
db_session.commit()

we = db_session.query(NewWallet).filter_by(status=0).all()
for i in we:
    print(i.address)


