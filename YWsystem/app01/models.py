from django.db import models

# Create your models here.

# 用户表

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)


# 业务表

class Application(models.Model):
    caption = models.CharField(max_length=128)


# 运维人员信息表

class YWUser(models.Model):
    username = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=32)


# 主机表

class Host(models.Model):
    server_ip = models.CharField(max_length=32)
    server_type = models.CharField(max_length=128)
    server_os_type = models.CharField(max_length=128)
    server_to_app = models.ForeignKey(to="Application",to_field="id",on_delete=models.CASCADE,related_name="app_to_server")
    server_to_yw_user = models.ForeignKey(to="YWUser",to_field="id",on_delete=models.CASCADE,related_name="yw_user_to_server")







