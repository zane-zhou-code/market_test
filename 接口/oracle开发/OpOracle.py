#coding=utf-8
import cx_Oracle
class OpOracle():
    def __init__(self,ora_username,ora_password,ora_host,ora_port,ora_sid):
        '''初始化Oracle连接'''
        self.db=cx_Oracle.connect(ora_username,ora_password,ora_host+':'+ora_port+'/'+ora_sid)
        self.cur=self.db.cursor()
    def Ora_Select(self,strSql):
        '''执行strSql语句进行查询'''
        self.cur.execute(strSql)
        return self.cur.fetchall()
    def Ora_IUD_Single(self,strSql):
        '''执行strSql语句进行增加、删除、修改操作'''
        self.cur.execute(strSql)
        self.db.commit()
    def Ora_IUD_Multi(self,strSql,List):
        '''执行strSql语句进行增加、删除、修改操作，对应参数使用List中的数据'''
        self.cur.prepare(strSql)
        self.cur.executemany(None,List)
        self.db.commit()
    def Ora_Cur_Close(self):
        '''关闭游标'''
        self.cur.close()
    def Ora_db_Close(self):
        '''关闭Oracle数据库连接'''
        self.db.close()
