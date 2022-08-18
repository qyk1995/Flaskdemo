from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask
import os
dbpath = os.getcwd()

dburl = 'sqlite:///' + dbpath + '/data.db'
engine = create_engine(dburl)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

SQLALCHEMY_TRACK_MODIFICATIONS = False
Base = declarative_base()
Base.query = db_session.query_property()
app = Flask(__name__)

def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import apps
    Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


init_db()