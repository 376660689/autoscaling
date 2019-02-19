from digital import digital
from setting import digital_CONF
from setting import mysql_CONF
from setting import qps_CONF
from db import MySql
from setting import logging
from share import write_droplet_db


from urllib.parse import urljoin
import requests
import math

class Error(Exception):
    pass

class ValueEmpty(Exception):
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
        ##获取一个ha的总qps##############################################################################
        single_program_qps = {}
        ServerNamekey = ''
        SecondsSinceLast = 0
        AverageReqTimeSec = 0
        RequestCount = 0
        RequestsPerSecs = 0
        xx5num = 0

        ###将项目下的所有droplet(通过autoscaling程序新建的)信息写入mysql####################################
        write_droplet_db(tag="%s_autoscaling" % program_name,
                         token=digital_CONF.token,
                         group=program_name,
                         dbconn=dbconn
                         )
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
        change_droplet_num = 0
        logging.debug("{}" % ())

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
            DIGITAL_OBJ.create_mul_droplets(tag=program_name, number=change_droplet_num)

        elif change_droplet_num < 0:
            delete_droplet_ids = get_delete_id(program_name, -change_droplet_num, dbconn=dbconn)
            if delete_droplet_ids:
                if -change_droplet_num >= len(delete_droplet_ids):
                    for delete_droplet_id in delete_droplet_ids:
                        DIGITAL_OBJ.delete_droplet(delete_droplet_id[0])
                else:
                    for index in range(-change_droplet_num):
                        logging.debug("delete droplet ids %s, index %s" % (delete_droplet_ids, index))
                        d_status = DIGITAL_OBJ.delete_droplet(delete_droplet_ids[index][0])
                        if d_status:
                            dbconn.delete(table='hosts', where={'hostid': delete_droplet_ids[index][0]})

        ###############################################################################################