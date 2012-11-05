=============================
Horizon (OpenStack Dashboard)
=============================

ChinaHorizon is based on Horizon project.

Author: Lion
Contact Email: 11315889@qq.com
QQ: 11315889

About Horizon:
http://github.com/openstack/horizon

SimpleBill
-----------------------------------------------------------------
活跃的云主机: 5 Active RAM: 56GB 本月的 VCPU 小时时间: 1479.95 本月的 GB 小时时间: 1039712.65
-----------------------------------------------------------------
计费项目    |   单价(每小时)     |  使用总时间(小时)   |   总费用      |
-----------------------------------------------------------------
VCPU       |    1/VCPU        |   1000           |    1000      |
-----------------------------------------------------------------
RAM        |    2/GB          |   1000           |    2000      |
-----------------------------------------------------------------
DISK       |    0.01/GB       |   10000          |    100       |
-----------------------------------------------------------------
合计        |                                     |     3100     |
-----------------------------------------------------------------

Bill DB:
(部分参考:https://github.com/sinacloud/dough)

class bills(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    region=models.CharField(max_length=200)
    payment_type =models.CharField(max_length=200)
    order_unit = models.CharField(max_length=200)
    order_size = models.IntegerField()
    price =models.FloatField()
    enabled=models.BooleanField(default=True)

class bill_users(models.Model):
    username = models.CharField(max_length=200,unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    password=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    company=models.CharField(max_length=200)
    real_name=models.CharField(max_length=200)
    ID_Card=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    qq=models.CharField(max_length=200,blank=True,null=True)
    account=models.FloatField(default=0.00,null=True)
    enabled=models.BooleanField(default=True)
    