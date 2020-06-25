from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

connection_string = 'mysql+pymysql://root@localhost:3306/cuandollego'
engine = create_engine(connection_string)


