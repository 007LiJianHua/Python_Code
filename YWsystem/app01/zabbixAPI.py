import requests
import json
import sys

url = "http://192.168.152.11/zabbix/api_jsonrpc.php"
user = "Admin"
password= "zabbix"
header = {"Content-Type":"application/json-rpc"}


# 发送POST请求

def sendPOST(data):
    try:
        r = requests.post(url=url, headers=header,data=json.dumps(data))
    except Exception as e:
        print("请求发送失败" + str(e))
        sys.exit()
    return json.loads(r.text)



# 用户登录，获取用户token

def userLogin():
    data = {
        "jsonrpc":"2.0",
        "method":"user.login",
        "params":{
            "user": user,
            "password":password
        },
        "id":1,
    }

    result = sendPOST(data=data)
    return result.get("result")


# 获取主机组ID

def get_host_group(group_name):
    user_token = userLogin()
    data = {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "extend",
            "filter": {
                "name": [
                    group_name
                ]
            }
        },
        "auth": user_token,
        "id": 2
    }
    result = sendPOST(data)
    return result.get("result")[0].get("groupid")


# 获取模板ID

def get_template():
    user_token = userLogin()
    data = {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "extend",
            "filter": {
                "host": [
                    "Template OS Linux"
                ]
            }
        },
        "auth": user_token,
        "id": 3
    }

    result = sendPOST(data)
    return result.get("result")[0].get("templateid")


# 创建监控主机

def create_zabbix_host(server_ip):
    user_token = userLogin()
    hostgroup = get_host_group("Zabbix servers")
    template = get_template()

    data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": server_ip,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": server_ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": hostgroup
                }
            ],
            "templates": [
                {
                    "templateid": template
                }
            ]
        },
        "auth": user_token,
        "id": 1
    }

    result = sendPOST(data)


if __name__ == '__main__':
    get_host_group()