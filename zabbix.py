# coding:utf-8

import requests
import json

class ZabbixApi:
    def __init__(self, api_url=False, user=None, passwd=None):
        self.auth_header = {'Content-Type': 'application/json-rpc'}
        auth_data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": user,
                "password": passwd,
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
            return res

    def post(self, url, data):
        try:
            if isinstance(data, dict) and len(data) != 0:
                res = requests.post(url, headers=self.auth_header, data=json.dumps(data))
                try:
                    if res.status_code > 210 or res.status_code < 200:
                        logging.error(res.text)
                        return False
                    else:
                        return res
                except Exception as msg:
                    logging.error(msg)
                    return False
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
                return None
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

    def FinalCreateHost(self, hostname, groupname, ipaddr, templatename):
        if hostname and groupname and templatename and ipaddr:
            GroupId = self.GethostGroup(groupname)[u'groupid']
            TemplateID = self.GetTemplate(templatename)[u'templateid']

            if GroupId and TemplateID:
                res = self.CreateHost(hostname, GroupId, ipaddr, TemplateID)
                if res:
                    return res.text
                else:
                    return False
            else:
                logging.error('add %s faild' % ipaddr)
                return False
        else:
            logging.error('Loss parameter')
            return False

#if __name__ == '__main__':
#z = zabbix()
    #hostid = z.gethost('autoscaling_1')['hostid']
    #print z.deletehost(hostid)

#print z.CreateHost('tt', 'autoscaling', '68.183.107.9', 'Template OS Linux').text
#z=ZabbixApi(ZabbixApiConf.ApiUrl)
#print z.start('ttchris', 'autoscaling', '192.168.1.222', 'Template OS Linux')
#print z.CreateHost('ttt', '15', '192.168.1.222', '10001')
#print(z.GetTemplate('autoscaling'))

#z.createhost('autoscaling_1', hostgroupId, '123.206.50.63', templateId)
#    print templateId
#    print hostgroupId