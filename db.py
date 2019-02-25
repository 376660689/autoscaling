import pymysql

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
            raise ValueEmpty("args null table:%s key:%s values:%s" % (key, table, values))
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
            if where[index] == 'null':
                value.append('`%s` is null' % index)
            else:
                if isinstance(where[index], float) or isinstance(where[index], int):
                    value.append('`%s`=%s' % (index, where[index]))
                else:
                    value.append('`%s`="%s"' % (index, where[index]))
        sql = "select %s from `%s` where %s" % (','.join(key), table, ' and '.join(value))

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