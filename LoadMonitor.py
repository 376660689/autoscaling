#coding:utf-8

import pymysql
import logging
import re

from setting import ZabbixMysql

ZabbixMysqlConf = ZabbixMysql()
logging.basicConfig(
    level=ZabbixMysqlConf.level,
    format=ZabbixMysqlConf.format,
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename=ZabbixMysqlConf.logs,
    filemode='a'
)

class zabbix:
    def __init__(self, host=None, user=None, passwd=None, db=None, port=3306):
        self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
        self.cur = self.conn.cursor()

    def LoadCpu(self, hosts={'sasha-db2': '128.199.210.122'}):
        '''
        最近半小时cou平均空闲百分比
        :param host:
        :return:
        '''

        LoadList = {}
        for host in hosts:
            try:
                if len(host)!=0:
                    sql = 'select value from history ' \
                        'where' \
                        ' itemid=(' \
                        'select itemid from items left outer join hosts ' \
                        'on items.hostid=hosts.hostid ' \
                        'where hosts.host="%s" and items.key_="system.cpu.util[,idle]")' \
                        ' order by clock desc limit 30' % host
                    self.cur.execute(sql)
                else:
                    logging.warning('parameter error!')
                    return False
            except Exception as msg:
                logging.error(msg)
                return False
            else:
                results = self.cur.fetchall()
                total = 0
                for res in results:
                    total = total + res[0]
                LoadList[host] = total/len(results)
        return LoadList

    def LoadMem(self, hosts={'sasha-db2': '128.199.210.122'}):
        '''
        最近半个小时的剩余内存的平均数,单位M
        :param host:
        :return:
        '''

        LoadList = {}
        for host in hosts:
            try:
                if len(host)!=0:
                    sql = 'select value from history_uint ' \
                          'where ' \
                          ' itemid=(' \
                          'select itemid from items left outer join hosts ' \
                          'on items.hostid=hosts.hostid ' \
                          'where hosts.host="%s" and items.key_="vm.memory.size[available]")' \
                          ' order by clock desc limit 30' % host
                    self.cur.execute(sql)
                else:
                    logging.warning('parameter error!')
                    return False
            except Exception as msg:
                logging.error(msg)
                return False
            else:
                results = self.cur.fetchall()
                total = 0
                for res in results:
                    total = total + res[0]
                LoadList[host] = total/len(results)/1024/1024
        return LoadList

    def __del__(self):
        self.conn.close()

#z=zabbix(host=ZabbixMysqlConf.host, user=ZabbixMysqlConf.user, passwd=ZabbixMysqlConf.passwd, db=ZabbixMysqlConf.db, port=ZabbixMysqlConf.port)
#print z.LoadCpu()
#print z.LoadMem()

#查 hostid select * from hosts
#查 groupid select * from groups
#