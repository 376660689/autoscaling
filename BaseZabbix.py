
def exist_group(obj, group_name):
    group_id = obj.hostgroup.get(filter={"name": group_name}, output="hostgroupid")
    if group_id:
        return group_id[0].get("groupid")
    else:
        create_group_info = obj.hostgroup.create(name=group_name)
        if create_group_info:
            return create_group_info.get("groupids")[0]
        else:
            return []

def exist_template(obj, template_name):
    template_id = obj.template.get(filter={"host": template_name}, output="templateid")
    if template_id:
        return template_id[0].get("templateid")
    else:
        return obj.template.get(filter={"host": "Template OS Linux"}, output="templateid")[0].get("templateid")

def create_host(obj, host_name, group_id, ipadd, templateid):
    create_host_info = obj.host.create(
        host=host_name,
        interfaces=[
            {
            "type":1,
            "main":1,
            "useip":1,
            "ip":ipadd,
            "dns":"",
            "port":'10050'
            }
        ],
        groups=[
            {
            "groupid": group_id
            }
        ],
        templates=templateid,
    )
    return create_host_info

def get_hostid(obj, group_name):
    group_id = obj.hostgroup.get(filter={"name": group_name}, output="groupid")
    if group_id:
        host_ids = obj.host.get(groupids= group_id[0].get("groupid"))
        host_id_dict = {}
        for host_info in host_ids:
            host_id_dict[host_info["hostid"]] = host_info["host"]
        return host_id_dict

def delete_host(obj, host_id):
    return obj.host.delete(host_id) if host_id else []
