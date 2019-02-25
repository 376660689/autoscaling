from zabbix import *
from setting import mysql_CONF
from setting import digital_CONF
from setting import qps_CONF
from setting import logging
from db import MySql
from share import PublicIsNull
import time

def check_full(dbconn=dbconn, exist_program={}):
    if dbconn and program_name:
        half_group = dbconn.select(table='hosts', key='group', where={'public': 'null'})
        if half_group:
            program_names = []
            for program_name in [g[0] for g in group]:
                if program_name not in program_names and program_name in exist_program.keys:
                    program_names.append(program_name)
            return program_names
        else:
            return []
    else:
        return []

if __name__ == "__main__":
    dbconn = MySql(host=mysql_CONF.host, user=mysql_CONF.user, passwd=mysql_CONF.passwd, port=mysql_CONF.port, db=mysql_CONF.db)
    for program_name in half_groups:
        PublicIsNull(group=program_name,
                token=digital_CONF.token,
                dbconn=dbconn
        )

    half_groups = check_full(dbconn=dbconn, program_name=qps_CONF.interface)
    if half_groups:
        pass