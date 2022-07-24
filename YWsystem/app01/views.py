from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01.API_test import *
import json
from app01 import zabbixAPI
from app01 import CobblerAPI
# Create your views here.

# 用户登录

def login(request):
    error_msg = ""
    if request.method == "GET":
        return render(request, "login.html", {"error_msg":error_msg})
    elif request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user_is_exist = models.User.objects.filter(username=user, password=pwd)
        if user_is_exist:
            res = redirect("/index/?username=%s" % user)
            from app01 import getcookie
            data = getcookie.randomString()
            import datetime
            start_time=datetime.datetime.utcnow()
            end_time = start_time + datetime.timedelta(days=1)
            res.set_cookie("token",data,expires=end_time)
            return res

        else:
            error_msg = "用户名或密码错误"
            return render(request, "login.html", {"error_msg":error_msg})


# 用户注册

def register(request):
    user_error_msg = ""
    pwd_error_msg = ""
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        user = request.POST.get("user")
        user_is_exist = models.User.objects.filter(username=user)
        if user_is_exist:
            user_error_msg = "用户已存在"
            return render(request, "register.html", {"user_error_msg":user_error_msg})
        else:
            pwd1 = request.POST.get("pwd1")
            pwd2 = request.POST.get("pwd2")
            if pwd1 != pwd2:
                pwd_error_msg = "密码不一致"
                return render(request, "register.html", {"pwd_error_msg": pwd_error_msg})
            else:
                models.User.objects.create(username=user, password=pwd2)
                return redirect("/login/")


# 显示主机管理主页

def index(request):
    if request.method == "GET":
        # 获取当前登录用户名
        username = request.GET.get("username")
        # 获取所有业务
        apps = models.Application.objects.all()
        # 获取所有服务器信息
        servers = models.Host.objects.all()
        data = request.COOKIES.get("token")
        if data:
            return render(request, "index.html", {"username":username, "apps":apps, "servers":servers})
        else:
            return redirect("/login/")


# 按业务显示主机

def showhost(request,app_id):
    apps = models.Application.objects.all()
    if app_id == "0":
        servers = models.Host.objects.all()
    else:
        servers = models.Host.objects.filter(server_to_app=app_id)

    data = request.COOKIES.get("token")
    if data:
        return render(request, "index.html", {"servers": servers, "apps": apps})
    else:
        return redirect("/login/")


# 添加新主机

def addhost(request):

    if request.method == "GET":
        apps = models.Application.objects.all()
        username = request.GET.get("username")
        yws = models.YWUser.objects.all()
        data = request.COOKIES.get("token")
        if data:
            return render(request, "addserver.html",{"apps":apps, "yws":yws,"username":username})
        else:
            return redirect("/login/")
    elif request.method == "POST":
        server_ip = request.POST.get("server_ip")
        server_type = request.POST.get("server_type")
        server_os_type = request.POST.get("server_os_type")
        server_to_app = request.POST.get("server_to_app")
        server_to_yw_user = request.POST.get("server_to_yw_user")
        server_monitor = request.POST.get("monitor")

        print(server_to_yw_user,server_to_app)
        print(server_ip, server_type, server_monitor, server_os_type, server_to_yw_user,server_to_app)

        if server_monitor == "1":
            zabbixAPI.create_zabbix_host(server_ip)

        app_obj = models.Application.objects.get(id=server_to_app)
        yw_obj = models.YWUser.objects.get(id=server_to_yw_user)

        new_host = {
            "server_ip":server_ip,
            "server_type":server_type,
            "server_os_type":server_os_type,
            "server_to_app":app_obj,
            "server_to_yw_user":yw_obj
        }
        models.Host.objects.create(**new_host)
        return redirect("/showhost-0/")


# 部署机器
def createhost(request):
    p1 = CobblerAPI.CobblerAPI(cobbler_url="http://192.168.78.10/cobbler_api", cobbler_user="cobbler",
                               cobbler_pwd="cobbler")
    if request.method == "GET":
        os = CobblerAPI.CobblerAPI.getProfile(self=p1)
        data = request.COOKIES.get("token")
        if data:
            return render(request, "createhost.html",{"os":os})

        else:
            return redirect("/login/")
    elif request.method == "POST":
        install = request.POST.get("install")
        server_name = request.POST.get("server_name")
        mac_ip = request.POST.get("mac_ip")
        choice_os = request.POST.get("choice_os")

        # os = models.Os.objects.filter(id=choice_os)

        # print(type(choice_os))
        print(install,server_name,mac_ip,choice_os)
        # print(type(os))
        # print(os.name_os)
        if  install == "1":
            p1.makeSystem(mac=mac_ip,profile_name=choice_os,system_name=server_name)
        return redirect("/showhost-0/")


#删主机

def remove(request):
    ip = request.GET.get("server_ip")
    # print(HttpResponse(ip))
    models.Host.objects.filter(server_ip=ip).delete()
    return redirect("/index")


# 显示主机详情

def hostdetail(request):
    server_ip = request.GET.get("server_ip")
    server_app = request.GET.get("server_app")
    server_yw_user = request.GET.get("server_yw")
    yw_phone = request.GET.get("yw_phone")
    yw_email = request.GET.get("yw_email")

    import paramiko

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip, username="root", password="redhat", port=22)

    stdin,stdout,stderr = ssh_client.exec_command("cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c ")
    cpu_model = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command("getconf LONG_BIT")
    cpu_arch = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command('dmidecode | grep "Product Name"')
    os_platform = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command('dmesg | grep -i eth')
    net_info = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command('uname -a')
    kernel_info = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command('lsblk')
    disk_info = stdout.read().decode("utf-8").replace("\n", "<br />")

    stdin, stdout, stderr = ssh_client.exec_command("sed -n '1,5p' /proc/meminfo")
    mem_info = stdout.read().decode("utf-8").replace("\n", "<br />")

    ssh_client.close()

    return render(
        request,
        "hostdetail.html",
        {
            "server_ip":server_ip,
            "server_app": server_app,
            "server_yw_user":server_yw_user,
            "yw_phone":yw_phone,
            "yw_email":yw_email,
            "cpu_model":cpu_model,
            "cpu_arch":cpu_arch,
            "os_platform":os_platform,
            "net_info":net_info,
            "kernel_info":kernel_info,
            "disk_info":disk_info,
            "mem_info":mem_info
        }
    )


# 显示发布系统

def push(request):
    if request.method == "GET":
        hosts = models.Host.objects.all()
        apps = models.Application.objects.all()
        username = request.GET.get("username")
        data = request.COOKIES.get("token")
        if data:
            return render(request, "push.html", {"username": username, "hosts": hosts, "apps": apps})

        else:
            return redirect("/login/")
    elif request.method == 'POST':
        project_file = request.FILES.get("project_file")
        project_path = request.POST.get("project_path")
        #print(project_file, project_path)

        # 接收文件
        src_file = "D:/YWsystem/YWsystem/upload/%s" % project_file.name

        with open(src_file, "wb") as f_obj:
            for data in project_file.chunks():
                f_obj.write(data)

        dst_file = project_path + "/" + project_file.name

        # 获取当前所选主机IP
        ip_list = []
        print("-----"*10)
        print(request.GET.get("app_id"))
        print("-----" * 10)
        app_obj = models.Application.objects.get(id=request.GET.get("app_id"))

        for server_obj in app_obj.app_to_server.all():
            ip_list.append(server_obj.server_ip)

        import paramiko
        result = []
        for ip in ip_list:
            try:
                ssh_client = paramiko.Transport((ip, 22))
            except Exception as e:
                msg = "服务器%s连接失败, 原因：%s" % (ip, str(e))
                result.append(msg)
                continue
            ssh_client.connect(username="root", password="redhat")
            ftp_client = paramiko.SFTPClient.from_transport(ssh_client)
            ftp_client.put(src_file, dst_file)
            ssh_client.close()
            msg = "服务器%s发送成功" % ip
            result.append(msg)

        return render(request, "push_result.html", {"result":result})

# 发布系统按业务显示主机

def push_showhost(request,app_id):
    apps = models.Application.objects.all()
    if app_id == "0":
        hosts = models.Host.objects.all()
    else:
        hosts = models.Host.objects.filter(server_to_app=app_id)
    return render(request,"push.html", {"hosts":hosts, "apps":apps, "app_id":app_id})



# 批量执行任务

def job(request):

    modules = {
        "1":"cmd.run",
        "2":"pkg.install"
    }

    if request.method == "GET":
        hosts = models.Host.objects.all()
        apps = models.Application.objects.all()
        username = request.GET.get("username")
        data = request.COOKIES.get("token")
        if data:
            return render(request, "execcmd.html", {"username": username, "hosts": hosts, "apps": apps})

        else:
            return redirect("/login/")
    elif request.method == "POST":
        module_name = request.POST.get("module_name")
        module_args = request.POST.get("module_args")
        print(module_args)
        print("-----" * 10)
        print(module_name, modules.get(module_args))
        # 获取当前所选主机IP
        print("-----" * 10)
        ip_list = []
        print(request.GET.get("app_id"))
        print("-----"*10)
        app_obj = models.Application.objects.get(id=request.GET.get("app_id"))
        for server_obj in app_obj.app_to_server.all():
            ip_list.append(server_obj.server_ip)


        # 调取salt-api执行任务

        all_result = []
        for ip in ip_list:
            result = salt_exec_command(ip, modules.get(module_name), module_args)
            all_result.append(result)


        # 将多行命令结果中的\n换为html中的换行符<br />
        new_result = []
        for i in all_result:
            tmp = json.dumps(i).replace(r'\n','<br />')
            new_result.append(json.loads(tmp))

        # print(new_result)
        hosts = models.Host.objects.all()
        apps = models.Application.objects.all()
        return render(request, "execcmd.html", {"all_result":new_result,"hosts":hosts, "apps":apps})


# 任务管理按业务显示主机

def job_showhost(request,app_id):
    apps = models.Application.objects.all()
    if app_id == "0":
        hosts = models.Host.objects.all()
    else:
        hosts = models.Host.objects.filter(server_to_app=app_id)
    return render(request,"execcmd.html", {"hosts":hosts, "apps":apps, "app_id":app_id})




# 显示所有业务

def showapp(request):
    if request.method == "GET":
        apps = models.Application.objects.all()
        data = request.COOKIES.get("token")
        if data:
            return render(request, "app_show.html", {"apps": apps})

        else:
            return redirect("/login/")
    elif request.method == "POST":
        app_name = request.POST.get("app_name")
        models.Application.objects.create(caption=app_name)
        return redirect("/showapp/")













