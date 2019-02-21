import digitalocean
from setting import digital_CONF
import time

DIGITAL_CONF_OBJ = digital_CONF()

class Error(Exception):
    pass

class ValueEmpty(Exception):
    pass

class DeleteFaild(Exception):
    pass

class digital:
    def __init__(self, token):
        self.token = token
        self._DIGITAL_MANAGE_OBJ = digitalocean.Manager(token=self.token)
        self._DIGITAL_DROPLET_OBJ = digitalocean.Droplet()

    def __droplet_info(self, data):
        values = {}
        for droplet_info in data:
            values[droplet_info.id] = {
                "hostname": droplet_info.name,
                "public": 'null' if droplet_info.ip_address is None else droplet_info.ip_address,
                "private": 'null' if droplet_info.private_ip_address is None else droplet_info.private_ip_address,
                "size_slug": droplet_info.size_slug,
                "region": droplet_info.region["slug"],
                "tags": droplet_info.tags[0],
                "snapshot_ids": droplet_info.snapshot_ids[0] if droplet_info.snapshot_ids else -1
            }
        return values

    def tag_droplets(self, tag):
        droplets = self._DIGITAL_MANAGE_OBJ.get_all_droplets(tag_name=tag)
        if droplets:
            return self.__droplet_info(droplets)
        else:
            return {}

    def id_droplet(self, droplet_id):
        if not droplet_id:
            raise ValueEmpty("droplet_id not allowd empty")
        return self._DIGITAL_MANAGE_OBJ.get_droplet(droplet_id=droplet_id)

    def create_mul_droplets(self, tag, number):
        if not tag and not number:
            raise ValueEmpty("args is empty")

        names = ["%s-%s" % (tag, time.time()) for j in range(number)]
        template = self.tag_droplets(tag)
        if template and len(template) == 1:
            for hostid in template:
                droplets = self._DIGITAL_DROPLET_OBJ.create_multiple(
                    token=self.token,
                    names=names,
                    size_slug=template[hostid]["size_slug"],
                    image=template[hostid]["snapshot_ids"],
                    region=template[hostid]["region"],
                    tags=["%s_autoscaling" % tag],
                    monitoring=True,
                    private_networking=True
                )
                return droplets if droplets else []
        else:
            raise ValueEmpty("template droplet is too many")

    def delete_droplet(self, id):
        if not id:
            raise ValueEmpty("args is null")

        droplet = self._DIGITAL_MANAGE_OBJ.get_droplet(id)
        if droplet.destroy():
            return True
        else:
            raise DeleteFaild("delete droplet faild!")


#a=digital(DIGITAL_CONF_OBJ.token).tag_droplets('rmroot_autoscaling')
#print(a)
#a=digital(DIGITAL_CONF_OBJ.token).create_mul_droplets('rmroot', 2)
#a=digital(DIGITAL_CONF_OBJ.token).delete_droplet(133104904,)
