import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename="/tmp/test.log",
    filemode="a"
)

class qps_CONF:
    interface = {
        "rmroot":[
                "http://localhost:6080/?domain=",
                [
                    "www.rm-root.com",
                ]
        ],
        "localhost":[
            "http://localhost:6080/?domain=",
            [
                "localhost",
            ]
        ],
    }
    maxlimit = 30   #增加机器的qps阀值requests/台机(当qps大于该值时增加机器)
    minlimit = 10    #减少机器的qps阀值requests/台机(增加机器时,将qps保持为该值)
    normalimit = 20  #将每台qps保持为该值
    #最大的机器数量
    maxserver = {
        "rmroot": 10
    }
    #不在自动增减范围的机器数量,key为项目名,必须和上面interface的key一致
    retain = {
        "rmroot": 1,
        "localhost": 1,
    }

class mysql_CONF:
    host = "localhost"
    user = "root"
    passwd = "XB2henshui%"
    port = 3306
    db = "autoscaling"

class digital_CONF:
    token = "126b2275fd7b10f30a81891d0d7749f91f000056c80187f0a584313d68bc"

class zabbix_CONF:
    url = "http://128.199.233.164/zabbix/api_jsonrpc.php"
    template = {
        "rmroot": "rmroot_template"
    }
