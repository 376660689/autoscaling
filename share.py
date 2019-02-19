from digital import digital
from setting import logging

def write_droplet_db(tag=None, token=None, group=None, dbconn=None):
    '''save droplet info to mysql'''
    digital_manager = digital(token)
    db_manager = dbconn

    #获取项目下的所有机器
    droplets = digital_manager.tag_droplets(tag)
    exist_droplet_ids = []
    if droplets:
        data = []
        for public in droplets:
            exist_droplet_ids.append(droplets[public]["hostid"])
            res = db_manager.select(table="hosts", key=['public',], where={"public": public})
            if not res:
                data.append(
                    (
                     droplets[public]["hostname"],
                     droplets[public]["hostid"],
                     public,
                     droplets[public]["private"],
                     droplets[public]["size_slug"],
                     droplets[public]["region"],
                     droplets[public]["tags"],
                     droplets[public]["snapshot_ids"] if droplets[public]["snapshot_ids"] else -1,
                     group,
                    )
                )
        logging.debug("insert table hosts %s" % data)
        #从数据库删除不存在的droplet信息
        droplet_in_dbs = dbconn.select(table='hosts', key=['hostid'], where={'group': group})
        if droplet_in_dbs:
            delete_droplet_mysql = []
            for droplet_in_db in droplet_in_dbs:
                if droplet_in_db[0] not in exist_droplet_ids:
                    dbconn.delete(table='hosts', where={'hostid': droplet_in_db[0]})
                    delete_droplet_mysql.append(droplet_in_db[0])
            logging.debug("delete from table hosts %s" % delete_droplet_mysql)

        #保存新建的droplet信息到mysql
        if data:
            ok = db_manager.insert(table="hosts",
                          key=["hostname", "hostid", "public", "private", "size", "region", "tags", "snapshotid", "group"],
                          values=data,
                        )
            if ok:
                return True
            else:
                return False

    else:
        dbconn.delete(table='hosts', where={'group': group})
        logging.debug("delete from hosts all droplet info where group=%s" % group)