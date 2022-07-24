import xmlrpc.client as xc
import sys

cobbler_url = "http://192.168.78.10/cobbler_api"
cobbler_user = "cobbler"
cobbler_pwd = "cobbler"
class CobblerAPI():
    # 构造函数, 接收cobbler api的地址， 用户名、密码
    def __init__(self, cobbler_url, cobbler_user, cobbler_pwd):
        self.cobbler_url = cobbler_url
        self.cobbler_user = cobbler_user
        self.cobbler_pwd = cobbler_pwd

    # 建立cobbler连接
    def cobblerCONN(self):
        try:
            conn = xc.Server(self.cobbler_url)
        except Exception as e:
            print("cobbler连接建立失败")
            print(e)
            sys.exit()
        return conn

    # 用户认证，获取令牌
    def getUserToken(self):
        conn = self.cobblerCONN()
        result = conn.login(self.cobbler_user, self.cobbler_pwd)
        return result

    # 获取cobbler服务器profile名称
    def getProfile(self):
        profile_list = []
        conn = self.cobblerCONN()
        profile = conn.get_profiles()
        for info in profile:
            profile_list.append(info.get("name"))
        return profile_list

    # 定制系统的功能
    def makeSystem(self, mac, profile_name, system_name):
        conn = self.cobblerCONN()
        user_token = self.getUserToken()

        # 创建定制系统对象
        system_obj = conn.new_system(user_token)
        # 定义定制系统的名称
        conn.modify_system(system_obj, "name", system_name, user_token)
        # 指定新服务器的MAC地址
        conn.modify_system(system_obj, "modify_interface", {
            "macaddress-eth0": mac
        }, user_token)
        # 指定绑定的系统名称
        conn.modify_system(system_obj, "profile", profile_name, user_token)

        conn.save_system(system_obj, user_token)
        conn.sync(user_token)

if __name__ == '__main__':
    p1 = CobblerAPI(cobbler_url="http://192.168.78.10/cobbler_api", cobbler_user="cobbler", cobbler_pwd="cobbler")

    print("cobbler服务器现有系统安装源如下: ")
    profile_list = p1.getProfile()
    for i in profile_list:
        print(i)
    print()
    mac_address = input("服务器MAC地址: ")
    while True:
        profile_name = input("绑定系统名称: ").strip()
        if profile_name not in profile_list:
            print("安装源'%s'不存在" % profile_name)
            continue
        else:
            break
    system_name = input("系统名称: ")
    p1.makeSystem(mac=mac_address, profile_name=profile_name, system_name=system_name)