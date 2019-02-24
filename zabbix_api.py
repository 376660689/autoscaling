from base import BaseApi


class ZabbixApi:
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get("host")
        self.user = kwargs.get("user")
        self.passwd = kwargs.get("passwd")
        self.timeout = kwargs.get("timeout")
        self.token = None
