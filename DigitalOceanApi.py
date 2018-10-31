#coding:utf-8
import requests
import json
import time
import math
import logging
from setting import DigitalApi

DigitalApiConf = DigitalApi()
logging.basicConfig(
	level=DigitalApiConf.level,
	format=DigitalApiConf.format,
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename=DigitalApiConf.logs,
	filemode='a'
)

class BaseDigital:
	def __init__(self, token):
		#token = '40f24fdf627963058a096e6a297b9963789dbdd3ad846df7bf9647202ec2c401'
		self.header = {
			'Authorization': 'Bearer %s' % token,
			'Content-Type': 'application/json',
		}

	def get(self, url):
		try:
			res = requests.get(url, headers=self.header)
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			return res.text

	def post(self, url, data):
		try:
			if isinstance(data, dict) and len(data) != 0:
				res = requests.post(url, headers=self.header, data=json.dumps(data))
				if res.status_code != 200:
					logging.error(res.text)
			else:
				logging.warning('post %s data is empty!' % url)
				return False
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			return True

class Droplet(BaseDigital):
	def __init__(self, token):
		BaseDigital.__init__(self, token)

	#列出所有服务器
	def ListAllDroplet(self):
		'''
		列出所有droplet
		:param arg:
		:return:
		'''
		try:
			url = 'https://api.digitalocean.com/v2/droplets'
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			res = self.get(url)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

	def ListTagDroplet(self,tag='auto1'):
		'''
			根据tags查找droplet
		:param arg:
		:return:
		'''
		try:
			url = 'https://api.digitalocean.com/v2/droplets?tag_name=%s' % tag
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			res = self.get(url)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

	def AddDroplet(self, **kwargs):
		'''
		通过快照创建dtoplet

		:param kwargs:
		name	实例名,字母数字组成
		region	地区,
			nyc1,2,3	纽约1区,2区,3区
			sgp1		新加坡1区
			sfo1,2		旧金山1区,2区
			ams2,3		阿姆斯特丹2区,3区
			lon1		伦敦1区
			fra1		法兰克福1区
			tor1		多伦多1区
			blr1		班加罗尔1区

		size	硬件配置
				s-1vcpu-3gb
				s-1vcpu-1gb
				s-1vcpu-2gb
				s-2vcpu-2gb
				s-3vcpu-1gb
				s-2vcpu-4gb
				s-4vcpu-8gb
				s-6vcpu-16gb

		image				镜像或快照的id,通过list出快照或镜像获取
		ssh_keys			密钥,None表示不设置
		backups				是否开启自动备份,True,False
		ipv6				是否支持ipv6,True,False
		user_data			初次运行时执行的脚本,一般是远程服务器上的,None表示无
		private_networking	是否开启内网ip,True,False
		monitoring			是否安装监控客户端do-agent
		volumes				挂载的硬盘,数组,硬盘id
		tags				实例的标签,用于分类

		:return:
		'''
		try:
			url = "https://api.digitalocean.com/v2/droplets"
			arg = ["name",
				   "region",
				   "size",
				   "image",
				   "ssh_keys",
				   "backups",
				   "ipv6",
				   "user_data",
				   "private_networking",
				   "monitoring"
				   "volumes",
				   "tags"
				   ]
			for k in arg:
				if k not in kwargs:
					return False

		except Exception as msg:
			raise msg
		else:
			res = self.post(url, kwargs)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

class SnapsHots(BaseDigital):
	def __init__(self, token):
		BaseDigital.__init__(self, token)

	def ListAllSnapshots(self):
		try:
			url = 'https://api.digitalocean.com/v2/snapshots'
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			res = self.get(url)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

	def ListDropletSnapshots(self):
		try:
			url = 'https://api.digitalocean.com/v2/snapshots?resource_type=droplet'
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			res = self.get(url)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

	def CreateSnapshots(self, snapshotname, dropletid):
		try:
			url = 'https://api.digitalocean.com/v2/droplets/%s/actions' % dropletid
			data = {"type": "snapshot", "name": snapshotname}
		except Exception as msg:
			logging.error(msg)
			return False
		else:
			res = self.post(url, data=data)
			if res:
				return json.loads(res)
			else:
				logging.warning(res.text)
				return False

#obj = SnapsHots(DigitalApiConf.token)
#print obj.ListAllSnapshots()
#print obj.ListDropletSnapshots()
#obj.SnapshotsToDroplet(name='auto_test',region="nyc1",size="s-1vcpu-1gb",image="39544156",ssh_keys=None,backups=False,ipv6=True,user_data=None,private_networking=True,volumes=None,tags=["auto",])
#obj = Droplet(DigitalApiConf.token)
#print obj.