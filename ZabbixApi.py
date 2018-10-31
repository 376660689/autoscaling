# coding:utf-8

import requests
import json
import logging
from setting import ZabbixApi

ZabbixApiConf = ZabbixApi()
logging.basicConfig(level=logging.DEBUG,
                    format=ZabbixApiConf.format,
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=ZabbixApiConf.logs,
                    filemode='a')

class ZabbixApi:
    def __init__(self, api_url=False):
        self.auth_header = {'Content-Type': 'application/json-rpc'}
        auth_data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": ZabbixApiConf.user,
                "password": ZabbixApiConf.passwd,
            },
            "id": 1,
            "auth": None
        }

        if api_url:
            self.auth_url = api_url
        else:
            self.auth_url = 'http://128.199.233.164/zabbix/api_jsonrpc.php'

        try:
            res = requests.post(self.auth_url, headers=self.auth_header, data=json.dumps(auth_data))
        except Exception as msg:
            self.auth = None
            logging.error(msg)
        else:
            self.auth = json.loads(res.text)['result']

    def get(self, url):
        try:
            res = requests.get(url, headers=self.auth_header)
        except Exception as msg:
            logging.error(msg)
            return False
        else:
            return res.text

    def post(self, url, data):
        try:
            if isinstance(data, dict) and len(data) != 0:
                res = requests.post(url, headers=self.auth_header, data=json.dumps(data))
                if res.status_code != 200:
                    logging.error(res.text)
            else:
                logging.warning('post %s data is empty!' % url)
                return False
        except Exception as msg:
            logging.error(msg)
            return False
        else:
            return res

    def GetHost(self, host):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "filter": {
                    "host": [
                        host,
                    ]
                }
            },
            "auth": self.auth,
            "id": 1
        }

        try:
            res = self.post(self.auth_url, data)
            if not res:
                logging.warning(res.text)
            else:
                return json.loads(res.text)[u'result'][0]

        except Exception as msg:
            logging.error(msg)
            return False

    def GethostGroup(self, hostgroup):
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [
                        hostgroup,
                    ]
                }
            },
            "auth": self.auth,
            "id": 1
        }

        try:
            res = self.post(self.auth_url, data=data)
            if not res:
                logging.warning(res.text)
            else:
                return json.loads(res.text)[u'result'][0]
        except Exception as msg:
            logging.error(msg)
            return False

    def GetTemplate(self, template):
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "extend",
                "filter": {
                    "host": [
                        template,
                    ]
                }
            },
            "auth": self.auth,
            "id": 1
        }

        try:
            res = self.post(self.auth_url, data=data)
            if not res:
                logging.warning(res.text)
            else:
                return json.loads(res.text)[u'result'][0]
        except Exception as msg:
            logging.error(msg)
            return False

    def CreateHost(self, host, groupid, ipaddr, templateid):
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ipaddr,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": groupid
                    },
                ],
                "templates": [
                    {
                        "templateid": templateid
                    },
                ],
            },
            "auth": self.auth,
            "id": 1
        }

        try:
            res = self.post(self.auth_url, data=data)
            if not res:
                logging.warning(res.text)
            else:
                return res
        except Exception as msg:
            logging.error(msg)
            return False

    def DeleteHost(self, hostid):
        try:
            if isinstance(hostid, list):
                params = hostid
            else:
                params = [hostid, ]

            if params and len(params)!=0:
                data = {
                    "jsonrpc": "2.0",
                    "method": "host.delete",
                    "params": params,
                    "auth": self.auth,
                    "id": 1
                }
            else:
                logging.warning('hostid is empty!')
                return False
        except Exception as msg:
            logging.error(msg)
            return False

        try:
            res = self.post(self.auth_url, data=data)
            if not res:
                logging.warning(res.text)
            else:
                return res
        except Exception as msg:
            logging.error(msg)
            return False

#if __name__ == '__main__':
    #z = zabbix()
    #hostid = z.gethost('autoscaling_1')['hostid']
    #print z.deletehost(hostid)


#    z = ZabbixApi()
#    templateId = z.GetTemplate(u'Template OS Linux')[u'templateid']
#    hostgroupId = z.GethostGroup(u'test')[u'groupid']
#    z.createhost('autoscaling_1', hostgroupId, '123.206.50.63', templateId)
#    print templateId
#    print hostgroupId