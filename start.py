#coding:utf-8

import pymysql
from __init__ import *
from setting import DigitalApi, ZabbixApi, ZabbixMysql

class Digital:
    def __init__(self):
        self.DigitalOceanApiConf = DigitalApi()
        self.DigitalOceanObj = DigitalOceanApi.Droplet(self.DigitalOceanApiConf.token)

    def DigitalOceanListTagDroplet(self, tag):
        TagDroplet = self.DigitalOceanObj.ListTagDroplet(tag=tag)
        if TagDroplet:
            return TagDroplet[u'droplets']
        else:
            return False

    def DigitalProject(self):
        return self.DigitalOceanApiConf.StandardMachine

if __name__ == '__main__':
    DigitalObj = Digital()

    for Project in DigitalObj.DigitalProject():
        Standard = 'Standard_%s' % DigitalObj.DigitalProject()[Project]
        DropletList = DigitalObj.DigitalOceanListTagDroplet(tag=DigitalObj.DigitalProject()[Project])

        for droplet in DropletList:
            print droplet[u'id']
            print droplet[u'snapshot_ids']