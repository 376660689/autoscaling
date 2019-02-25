from pyzabbix import ZabbixAPI
from setting import zabbix_CONF
from digital import digital
from setting import digital_CONF,qps_CONF
from setting import logging
from BaseZabbix import exist_template, exist_group, create_host, get_hostid, delete_host
import sys

if __name__ == "__main__":
    zabi = ZabbixAPI(zabbix_CONF.url)
    zabi.login(zabbix_CONF.user, zabbix_CONF.passwd)
    digital_obj = digital(digital_CONF.token)

    for program in qps_CONF.interface:
        group_id = exist_group(zabi, '%s_autoscaling' % program)
        template_id = exist_template(zabi, zabbix_CONF.template[program])
        droplets = digital_obj.tag_droplets("%s_autoscaling" % program)
        digital_host_names = [droplets[j].get("hostname") for j in droplets]

        for droplet_id in droplets:
            public = droplets.get(droplet_id).get('public')
            if public:
                digital_hostname = droplets.get(droplet_id).get("hostname")
                zabbix_host = zabi.host.get(filter={'host': digital_hostname})
                if not zabbix_host:
                    create_host_info = create_host(zabi, digital_hostname, group_id, public, template_id)
                    logging.info("create zabbix monitor host_name: %s sucess" % (digital_hostname))
                else:
                    logging.error("create zabbix monitor host_name: %s faild" % digital_hostname)

        zabbix_host_ids = get_hostid(zabi, '%s_autoscaling' % program)
        if zabbix_host_ids:
            for zabbix_host_id in zabbix_host_ids:
                if not zabbix_host_ids[zabbix_host_id] in digital_host_names:
                    delete_host(zabi, zabbix_host_id)