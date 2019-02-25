from digital import digital

class Error(Exception):
    pass

class ValueEmpty(Error):
    pass


def InDroletNotDb(token=None, dbconn=None, group=None):
    if not token or not dbconn or not group:
        raise ValueEmpty("token or dbconn or group is None")
    try:
        digital_manager = digital(token)
    except Exception as msg:
        raise msg

    digital_droplets = digital_manager.tag_droplets("%s_autoscaling" % group)
    if digital_droplets:
        db_droplets = dbconn.select(table='hosts', key=['hostid', ], where={'tags': "%s_autoscaling" % group})
        db_droplet_ids = [j[0] for j in db_droplets]

        droplet_not_in_db = []
        for hostid in digital_droplets:
            if hostid not in db_droplet_ids:
                droplet_not_in_db.append(
                    (
                        digital_droplets[hostid]["hostname"],
                        hostid,
                        digital_droplets[hostid]["public"],
                        digital_droplets[hostid]["private"],
                        digital_droplets[hostid]["size_slug"],
                        digital_droplets[hostid]["region"],
                        digital_droplets[hostid]["tags"],
                        digital_droplets[hostid]["snapshot_ids"] if digital_droplets[hostid]["snapshot_ids"] else -1,
                        group,
                    )
                )

        if droplet_not_in_db:
            insert_status = dbconn.insert(table="hosts",
                                key=["hostname",
                                     "hostid",
                                     "public",
                                     "private",
                                     "size",
                                     "region",
                                     "tags",
                                     "snapshotid",
                                     "group"],
                                values=droplet_not_in_db,
                              )
        else:
            return (True, "%s droplets all in group" % group)
        return (insert_status, droplet_not_in_db) if insert_status else (False, droplet_not_in_db)
    else:
        return (True, "group %s no living droplets" % group)

def InDbNotDroplet(token=None, dbconn=None, group=None):
    if not token or not dbconn or not group:
        raise ValueEmpty("args null token: %s dbconn: %s group: %s" % (token, dbconn, group))

    try:
        digital_manager = digital(token)
    except Exception as msg:
        raise msg

    digital_droplets = digital_manager.tag_droplets("%s_autoscaling" % group)
    digital_droplet_ids = [ j for j in digital_droplets ]
    if digital_droplet_ids:
        db_droplets = dbconn.select(table='hosts', key=['hostid', ], where={'tags': "%s_autoscaling" % group})

        sucess = ()
        faild = ()
        for db_droplet_id in db_droplets:
            if db_droplet_id[0] not in digital_droplet_ids:
                delete_status = dbconn.delete(table='hosts', where={'hostid': db_droplet_id[0]})
                if delete_status:
                    sucess.append(db_droplet_id[0])
                else:
                    faild.append(db_droplet_id[0])
            else:
                pass
        if faild:
            return (False, faild)
        else:
            return (True, sucess)

    else:
        if dbconn.delete(table='hosts', where={'tags': '%s_autoscaling' % group}):
            return (True, "group %s no living droplets" % group)
        else:
            return (False, "group %s droplet delete faild" % group)

def PublicIsNull(token=None, dbconn=None, group=None):
    print('###############################################')
    if not token or not dbconn or not group:
        raise "token or dbconn or group is None"

    try:
        digital_manager = digital(token)
    except Exception as msg:
        raise msg

    public_is_null = dbconn.select(table='hosts', key=['`hostid`', '`group`'],
                                   where={'public': 'null', 'tags': '%s_autoscaling' % group}
                                   )

    if public_is_null:
        droplets_info = []
        for hostid, group in public_is_null:
            digital_droplets = digital_manager.id_droplet(hostid)

            droplets_info.append(
                (
                    digital_droplets.name,
                    hostid,
                    digital_droplets.ip_address,
                    digital_droplets.private_ip_address,
                    digital_droplets.size_slug,
                    digital_droplets.region.get('slug'),
                    digital_droplets.tags[0],
                    digital_droplets.snapshot_ids[0] if digital_droplets.snapshot_ids else -1,
                    group,
                )
            )
        insert_status = dbconn.insert(table="hosts",
                                  key=["hostname",
                                       "hostid",
                                       "public",
                                       "private",
                                       "size",
                                       "region",
                                       "tags",
                                       "snapshotid",
                                       "group"
                                       ],
                                  values=droplets_info,
                                  )

        if insert_status:
            insert_status = (insert_status,
                                "%s %s" % (
                                    "hostname, hostid, public, private, size, region, tags, snapshotid, group",
                                    droplets_info
                                    )
                             )
        else:
            insert_status = (False,
                                "%s %s" % (
                                    "hostname, hostid, public, private, size, region, tags, snapshotid, group",
                                    droplets_info
                                    )
                            )
    else:
        insert_status = (True, "droplets info is full")

    return insert_status