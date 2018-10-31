#coding:utf-8
import logging

class BaseClass:
    def __init__(self):
        self.logs = '/tmp/test.log'
        self.format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        self.level = logging.DEBUG

class DigitalApi(BaseClass):
    def __init__(self):
        BaseClass.__init__(self)
        self.token = '40f24fdf627963058a096e6a297b9963789dbdd3ad846df7bf9647202ec2c401'
        self.header = {
            'Authorization': 'Bearer %s' % self.token,
            'Content-Type': 'application/json',
        }
        self.StandardMachine = {
            'Eu_KakaGames': 'AutoScaling_EU_KakaGames',
            'As_KakaGames': 'AutoScaling_AS_KakaGames',
            'Eu_Payment': 'AutoScaling_EU_Payment',
            'As_Payment': 'AutoScaling_AS_Payment',
            'As_AdServer': 'AutoScaling_AS_Adserver'
        }

class ZabbixApi(BaseClass):
    def __init__(self):
        BaseClass.__init__(self)
        self.ApiUrl = 'http://128.199.233.164/zabbix/api_jsonrpc.php'
        self.user = 'admin'
        self.passwd = 'zabbix'

class ZabbixMysql(BaseClass):
    def __init__(self):
        BaseClass.__init__(self)
        self.host = "128.199.233.164"
        self.user = "monitor"
        self.passwd = "XB2henshui%"
        self.db = "zabbix"
        self.port = 3306