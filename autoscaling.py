from digital import digital
from setting import digital_CONF
from setting import mysql_CONF
from setting import qps_CONF
from db import MySql
from setting import logging
from share import InDroletNotDb, InDbNotDroplet, PublicIsNull
from BaseZabbix import get_hostid, delete_host
from pyzabbix import ZabbixAPI
from setting import zabbix_CONF

from urllib.parse import urljoin
import requests
import math

class Error(Exception):
    pass

class ValueEmpty(Error):
    pass

class DataNotFull(Error):
    pass

def get_delete_id(program_name, number, dbconn):
    if not program_name or not number:
        raise ValueEmpty("args is null")
    db_manager = dbconn

    hostids = db_manager.select(table='hosts', key=['hostid'], where={'group': program_name})
    if hostids:
        return hostids
    else:
        return []

def get_qps(url):
    domain_qps = {}
    try:
        req = requests.get(url)
        if req.ok:
            qps_info = req.text.replace('\t', '').strip('\n').split('\n')
            for value in qps_info:
                field = value.split(":")
                domain_qps[field[0]] = field[1]
        else:
            domain_qps = []
        return domain_qps
    except Exception as msg:
        raise msg

if __name__ == "__main__":
    dbconn = MySql(host=mysql_CONF.host, user=mysql_CONF.user, passwd=mysql_CONF.passwd, port=mysql_CONF.port, db=mysql_CONF.db)

    #将droplet信息写入mysql
    for program_name in qps_CONF.interface:
        #检测数据库数据完整性
        not_db = InDroletNotDb(token=digital_CONF.token, dbconn=dbconn, group=program_name)
        not_digital = InDbNotDroplet(token=digital_CONF.token, dbconn=dbconn, group=program_name)
        is_null = PublicIsNull(token=digital_CONF.token, dbconn=dbconn, group=program_name)

        if not not_db[0]:
            logging.warning(not_db[1])
            raise DataNotFull(not_db[1])
        else:
            logging.debug(not_db[1])

        if not not_digital[0]:
            logging.warning(not_digital[1])
            raise DataNotFull(not_digital[1])
        else:
            logging.debug(not_digital[1])

        if not is_null[0]:
            logging.warning(is_null[1])
            raise DataNotFull(is_null[1])
        else:
            logging.debug(is_null[1])

        ##获取一个ha的总qps##############################################################################
        single_program_qps = {}
        ServerNamekey = ''
        SecondsSinceLast = 0
        AverageReqTimeSec = 0
        RequestCount = 0
        RequestsPerSecs = 0
        xx5num = 0

        ##############################################################################################
        for domain in qps_CONF.interface[program_name][1]:
            ##请求的域名
            url = urljoin(qps_CONF.interface[program_name][0], "?domain=%s" % domain)
            ##获取qps
            domain_qps = get_qps(url)

            ServerNamekey = "%s,%s" % (ServerNamekey, domain_qps["Server Name key"])
            SecondsSinceLast = SecondsSinceLast + float(domain_qps["Seconds SinceLast"])
            AverageReqTimeSec = AverageReqTimeSec + float(domain_qps["Average Req Time Sec"])
            RequestCount = RequestCount + float(domain_qps["Request Count"])
            RequestsPerSecs = RequestsPerSecs + float(domain_qps["Requests Per Secs"])
            xx5num = xx5num + float(domain_qps["5xx num"])
        ##################################################################################################

        ##获取新增和减少的droplet数量########################################################################
        droplets_in_group = dbconn.select(table="hosts", key=["hostid"], where={"group": program_name})

        #保存qps信息到mysql
        dbconn.insert(table='qps',
                      key=['servername',
                           'SecondsSinceLast',
                           'AverageReqTimeSec',
                           'RequestCount',
                           'RequestsPerSecs',
                           '5xxnum',
                           'group'],
                      values=[(
                          ServerNamekey,
                          SecondsSinceLast/(len(droplets_in_group)+qps_CONF.retain[program_name]),
                          AverageReqTimeSec/(len(droplets_in_group)+qps_CONF.retain[program_name]),
                          RequestCount/(len(droplets_in_group)+qps_CONF.retain[program_name]),
                          RequestsPerSecs/(len(droplets_in_group)+qps_CONF.retain[program_name]),
                          xx5num/(len(droplets_in_group)+qps_CONF.retain[program_name]),
                          program_name
                      ),]
                )

        change_droplet_num = 0

        AvgRequestsPerSecs = RequestsPerSecs/(len(droplets_in_group) + qps_CONF.retain[program_name])
        if AvgRequestsPerSecs > qps_CONF.maxlimit:
            change_droplet_num = math.ceil(RequestsPerSecs/qps_CONF.normalimit - (len(droplets_in_group) + qps_CONF.retain[program_name]))
        elif AvgRequestsPerSecs < qps_CONF.minlimit:
            change_droplet_num = math.ceil(RequestsPerSecs/qps_CONF.normalimit - (len(droplets_in_group) + qps_CONF.retain[program_name]))
        else:
            change_droplet_num = 0
        ##################################################################################################
        #print(RequestsPerSecs)
        #print(change_droplet_num)
        logging.debug("program %s change droplet number %s" % (program_name, change_droplet_num))

        ##添加或删除droplet##########################################################################
        DIGITAL_OBJ = digital(digital_CONF.token)
        if change_droplet_num > 0:
            add_droplets = DIGITAL_OBJ.create_mul_droplets(tag=program_name, number=change_droplet_num)

            dbconn.insert(table='hosts',
                           key=['hostname',
                                'region',
                                'size',
                                'hostid',
                                'public',
                                'group',
                                'tags',
                                ],
                           values=[
                               (
                                   j.name,
                                   j.region.get('slug'),
                                   j.size_slug,
                                   j.id,
                                   'null' if j.ip_address is None else j.ip_address,
                                   program_name,
                                   j.tags[0]
                                ) for j in add_droplets
                           ]

                    )

        elif change_droplet_num < 0:
            delete_droplet_ids = get_delete_id(program_name, -change_droplet_num, dbconn=dbconn)
            if delete_droplet_ids:
                zabi = ZabbixAPI(zabbix_CONF.url)
                zabi.login(zabbix_CONF.user, zabbix_CONF.passwd)

                if -change_droplet_num >= len(delete_droplet_ids):
                    for delete_droplet_id in delete_droplet_ids:
                        d_status = DIGITAL_OBJ.delete_droplet(delete_droplet_id[0])
                        if d_status:
                            dbconn.delete(table='hosts', where={'hostid': delete_droplet_id[0]})
                            logging.debug("delete droplet ids %s, index %s" % (delete_droplet_ids, delete_droplet_id))
                else:
                    for index in range(-change_droplet_num):
                        logging.debug("delete droplet ids %s, index %s" % (delete_droplet_ids, index))
                        d_status = DIGITAL_OBJ.delete_droplet(delete_droplet_ids[index][0])
                        if d_status:
                            dbconn.delete(table='hosts', where={'hostid': delete_droplet_ids[index][0]})
                            logging.debug("delete droplet ids %s, index %s" % (delete_droplet_ids, index))




    ###############################################################################################
        #检测数据库数据完整性
        not_db = InDroletNotDb(token=digital_CONF.token, dbconn=dbconn, group=program_name)
        not_digital = InDbNotDroplet(token=digital_CONF.token, dbconn=dbconn, group=program_name)
        is_null = PublicIsNull(token=digital_CONF.token, dbconn=dbconn, group=program_name)

        if not not_db[0]:
            logging.warning("%s %s" % (program_name, not_db[1]))
            raise DataNotFull("%s %s" % (program_name, not_db[1]))
        else:
            logging.debug("%s %s" % (program_name, not_db[1]))

        if not is_null[0]:
            logging.warning("%s %s" % (program_name, is_null[1]))
            raise DataNotFull("%s %s" % (program_name , is_null[1]))
        else:
            logging.debug("%s %s" % (program_name, is_null[1]))