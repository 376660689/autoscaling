from zabbix import *
from setting import mysql_CONF
from setting import digital_CONF
from setting import qps_CONF
from setting import logging
from db import MySql
from share import write_droplet_db
from

import time

def check_full(dbconn=dbconn, exist_program={}):
    if dbconn and program_name:
        half_group = dbconn.select(table='hosts', key='group', where={'public': 'null'})
        if half_group:
            program_names = []
            for program_name in [g[0] for g in group]:
                if program_name not in program_names and program_name in program_name.keys:
                    program_names.append(program_name)

            return program_names
        else:
            return []
    else:
        return []

if __name__ == "__main__":
    dbconn = MySql(host=mysql_CONF.host, user=mysql_CONF.user, passwd=mysql_CONF.passwd, port=mysql_CONF.port, db=mysql_CONF.db)
    for count in range(10):
        half_groups = check_full(dbconn=dbconn, program_name=qps_CONF.interface)
        if half_groups:
            for program_name in half_groups:
                write_droplet_db(tag="%s_autoscaling" % program_name,
                                 token=digital_CONF.token,
                                 group=program_name,
                                 dbconn=dbconn
                                 )
            logging.warning("Incomplete server information, %s" % half_group)
            time.sleep(60)
        else:
            break

    if not half_groups:
