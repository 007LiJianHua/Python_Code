# 调用salt-api执行任务

import requests
import json
import sys

'''
    通过requests向https主机发送POST请求时，可为其添加参数verify=False禁用证书
    但是，会造成每次产生ssl警告信息，下面这行代码是为了防止出现该警告信息
'''
requests.packages.urllib3.disable_warnings()



'''
    通过POST请求发送数据，并以字典的形式返回结果 
'''
def sendPOST(url, header, data):
    try:
        r = requests.post(url=url, data=json.dumps(data), headers=header, verify=False)
    except Exception as e:
        print("发送请求失败" + str(e))
        sys.exit()
    return json.loads(r.text)


'''
    获取用户令牌
'''
def get_user_token():
    salt_login_url = "https://192.168.78.20:8001/login"
    username = "admin"
    password = "redhat"
    header = {"Content-Type":"application/json"}
    data = {
        "username":username,
        "password":password,
        "eauth":"pam"
    }

    user_info = sendPOST(url=salt_login_url, data=data, header=header)
    return user_info.get("return")[0].get("token")


'''
    调用salt模块执行命令
    target参数：对哪些主机执行命令
    method：调用salt的模块名称
    arg：模块的参数
'''
def salt_exec_command(target, method, arg=None, client="local"):
    salt_exec_url = "https://192.168.78.20:8001"

    '''
        将salt用户的令牌封装到http首部，发送执行命令的请求
    '''
    user_token = get_user_token()
    header = {"X-Auth-Token": user_token, "Content-Type":"application/json"}

    if arg:
        data = {"client":client, "tgt":target, "fun":method, "arg":arg}
    else:
        data = {"client": client, "tgt": target, "fun": method}

    command_result = sendPOST(url=salt_exec_url, header=header, data=data)
    #print(command_result)

    '''
        格式化输出命令结果
    '''
    # for host, result in command_result.get("return")[0].items():
    #     print("主机名：%s" % host)
    #     print("命令结果:")
    #     print(result)
    #     print("---" * 10)
    return command_result.get("return")[0]




if __name__ == '__main__':
    # print(get_user_token())
    print(salt_exec_command("*", "cmd.run", "free -m"))



