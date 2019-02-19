import pymysql
import logging
class Error(Exception):
    pass

class ValueEmpty(Error):
    pass

class MySql:
    def __init__(self, host=None, user=None, passwd=None, port=3306, db='autoscaling'):
        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, db=db)
        self.cur = self.conn.cursor()

    def insert(self, table=None, key=[], values=[]):
        '''
            table  str  table name
            key    list index name      key=['index1', 'index2']
            values list data            values=[('field1', field2), ('fiedl1', field2)]
        '''
        if not key or not table or not values:
            raise ValueEmpty("args is null")
        sql = "replace into %s(%s) values(%s);" % (table, ','.join(['`%s`' % x for x in key]), ','.join(['%s' for x in key]))
        try:
            self.cur.executemany(sql, values)
            self.conn.commit()
        except Exception as msg:
            self.conn.rollback()
            raise msg
        else:
            return True

    def delete(self, table=None, where={}):
        if not table or not where:
            raise ValueEmpty("args is null")

        value = []
        for key in where:
            if isinstance(where[key], float) or isinstance(where[key], int):
                value.append('`%s`=%s' % (key, where[key]))
            else:
                value.append('`%s`="%s"' % (key, where[key]))
        sql = "delete from `%s` where %s" % (table, ' and '.join(value))
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as msg:
            self.conn.rollback()
            raise msg
        else:
            return True

    def select(self, table=None, key=['*'], where={}):
        if not table or not where:
            raise ValueEmpty("args is null")

        value=[]
        for index in where:
            if isinstance(where[index], float) or isinstance(where[index], int):
                value.append('`%s`=%s' % (index, where[index]))
            else:
                value.append('`%s`="%s"' % (index, where[index]))
        sql = "select `%s` from `%s` where %s" % (','.join(key), table, ' and '.join(value))

        try:
            self.cur.execute(sql)
            reslut = self.cur.fetchall()
        except Exception as msg:
            raise msg
        else:
            return reslut

    def __del__(self):
        self.cur.close()
        self.conn.close()

#con=MySql(host='localhost',user='root',passwd='XB2henshui%')
#con.insert(table='hostgroups', key=['groupname', 'groupid'], values=[('h1',3), ('h2',4 ), ('h3',5 )])
#con.delete(table='hostgroups', where={'groupid':5, 'groupname':'h3'})
#con.select(table="hostgroups", key=['groupid'], where={'groupid':2})
#con.insert(table='hosts', key=['hostname','hostid','public','private','size','region','tags','snapshotid','group'], values=[('template', 130740838, '157.230.218.131', 'null', 's-1vcpu-1gb', 'nyc1', 'rmroot', 43015793, 'rmroot')])