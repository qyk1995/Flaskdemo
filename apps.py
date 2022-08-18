from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String,Float,DateTime
from database import  Base
import os
from sqlalchemy.sql import func

from datetime import datetime
from flask_migrate import Migrate
from flask_script import Manager
app = Flask(__name__)

dbpath = os.getcwd()
print(dbpath)
dburl = 'sqlite:///' + dbpath + '/data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = dburl

manager = Manager(app)

db = SQLAlchemy(app)

migrate = Migrate(app,db)

class NewWallet(Base):
    __tablename__ = 'newwallets'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    address = Column(String(200), unique=True)
    status = Column(Integer)  # 标识新钱包是否使用
    create_time = Column(DateTime,  default=datetime.now())


    def __init__(self, address=None,status=None):
        self.address = address
        self.status = status



#记录历史转移热点记录
class Transfer(Base):
    __tablename__ = 'transfers'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    source_hotspots = Column(String(200))
    dest_wallet = Column(String(200))
    status = Column(Integer)  #
    create_time = Column(DateTime,  default=datetime.now())



    def __init__(self, source_hotspots=None,dest_wallet=None,status=None):
        self.source_hotspots = source_hotspots
        self.dest_wallet = dest_wallet
        self.status = status




# 展示历史记录，源钱包到目的钱包的转移金额的信息
class BalancePay(Base):
    __tablename__ = 'balances'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    source_wallet = Column(String(200))
    dest_wallet = Column(String(200))
    blance = Column(Float)
    status = Column(Integer)  #
    create_time = Column(DateTime,  default=datetime.now())



    def __init__(self, source_wallet=None,dest_wallet=None,blance=None,status= None):
        self.source_wallet = source_wallet
        self.dest_wallet = dest_wallet
        self.blance = blance
        self.status =status



db.create_all()
