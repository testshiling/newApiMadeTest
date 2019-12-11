# coding = utf-8


from apitest.models import *
from rest_framework.response import Response
import threading


# 支付第三方接口
def others_pay_order_true(**data):
    order_id = data['order_id']
    totalprice = data['totalprice']
    other_order_info = others_order.objects.filter(order_id=str(order_id))
    if other_order_info:
        pass
    else:
        others_order.objects.create(order_id=order_id)
    # 下面这步在实际中其实是不对，应该是从第三方库中查
    try:
        orderinfo = order.objects.filter(id=str(order_id))
    except Exception:
        return Response({"status_code": 400, "msg": "订单不存在"})
    for i in orderinfo:
        if totalprice == i.totalprice:
            if i.estate == 'valid':
                coo_others = threading.Thread(target=update_others_order, kwargs=({"order_id": order_id, "totalprice": totalprice, "estate": "yes"}))
                coo_others.start()
                coo_back = threading.Thread(target=payback_order_true, kwargs=({"order_id": order_id}))
                coo_back.start()
                return Response({"status_code": 200, "msg": "支付成功"})
            else:
                others_order.objects.filter(order_id=order_id).delete()
                return Response({"status_code": 400, "msg": "订单状态不正确"})
        else:
            return Response({"status_code": 400, "msg": "订单总价不正确"})


# 支付回调接口--第三方用
def payback_order_true(**data):
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='done')
    except Exception:
        return Response({"status_code": 400, "msg": "支付订单回调更新失败"})


# 起一个进程去后台更新数据库
def update_others_order(**data):
    check_dict = isinstance(data, dict)
    if check_dict:
        others_order.objects.filter(order_id=data['order_id']).\
            update(**data)
        pass
    else:
        return Response({"status_code": 400, "msg": "订单更新失败"})

    print("更新内容：" + str(data))


# 起一个进程去取消订单
def order_cancel(**data):
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='cancel')
    except Exception:
        return Response({"status_code": 400, "msg": "取消订单回调更新失败"})