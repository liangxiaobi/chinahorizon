=============================
Horizon (OpenStack Dashboard)
=============================

ChinaHorizon is based on Horizon project.

Author: Lion
Contact Email: 11315889@qq.com
QQ: 11315889

About Horizon:
http://github.com/openstack/horizon

Bill DB:
(部分参考:https://github.com/sinacloud/dough)

#计费地区
class bill_regions(models.Model):
    name =models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
# 扣费项目表
class bill_items(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
# 计费周期类型
# is_prepaid是预付费还是后付费
# interval_*是计费的周期
class bill_payment_types(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    interval_unit =models.CharField(max_length=200)
    interval_size = models.IntegerField()
    is_prepaid = models.IntegerField()
# 产品表
# order_*是费用单位, payment_types.interval*不能大于products.order*
# 目前payment_types.interval_* 和 products.order* 的时间周期必须全部一样
# 举例：
# payment_types.interval_*= 1 day , products.order*= 1 month, 则
# 举例：
# payment_types.interval_*= 1 hour , products.order*= 10Mb Bytes, 则一个小时之后产生一条 
#           purchases.quantity/products.order_size*products.price
# 的费用记录
# currency是货币单位，暂时没用
class bill_products(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    region_id=models.IntegerField()
    item_id=models.IntegerField()
    payment_type_id =models.IntegerField()
    order_unit = models.CharField(max_length=200)
    order_size = models.IntegerField()
    price =models.FloatField()
    currency=models.CharField(max_length=200)
# 订单表
# 创建resource如虚拟机的时候会生成一条记录
# project_id是用户的tenant_id
# resource_uuid 虚拟机的uuid或者loadblance的uuid等
# resource_name是用户起的名字
# expires_at是下一个计费的时间
# status是状态，对应内部的处理函数名称
# 资源被回收如虚拟机关闭、floatingip取消的时候会删除对应的subscriptions记录（仅标记deleted字段，不实际删除） 
class bill_journal(models.Model):
    name = models.CharField()
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    region_id=models.IntegerField()
    project_id=models.CharField()
    product_id=models.IntegerField()
    resource_uuid=models.CharField()
    resource_name=models.CharField()
    expires_at =models.DateTimeField()
    status=models.CharField()
# 扣费记录表
# 在每个收费点上都会生成一条记录
# 预付费的subscriptions会在creating改变为verify的时候生成一条记录
# 后付费的subscriptions会在从deleting变为terminated的时候生成一条记录
# 所有verify的subscriptions的expires_at大于当前时间就会生成一条记录
# quantity是当前计费周期内的数据量（流量单位目前为byte，floatingip等为天）
# line_total是本次费用
# 已经实际扣过费的记录，flag字段为1。未扣费的为0；扣费失败的为-1   
class bill_purchases(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    instance_id =models.IntegerField()
    quantity = models.FloatField()
    line_total = models.FloatField()
    flag = models.IntegerField()