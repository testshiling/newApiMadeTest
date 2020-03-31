from django.shortcuts import render,HttpResponse
from apitest.models import *
import json
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password, make_password
import sys
import datetime
import threading
from apitest.others import others_pay_order_true
import hashlib



# @csrf_exempt
# @api_view(http_method_names=['get'])
# @permission_classes((permissions.AllowAny,))
# def welcome(request):
#     return Response("一起来学习接口测试呀！")

# api_demo
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def api_demo(request):
    parameter = request.data
    id = parameter['data']
    if id == 1:
        data = 'There are three dogs'
    elif id == 2:
        data = 'There are two dogs'
    else:
        data = 'Thers is nothing'

    return Response({'data': data})


# 登录接口-post
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def login_post(request):
    data = json.loads(request.body)
    if "username" not in data:
        return Response({
            "status_code": 400,
            'msg': "请输入username"
        })
    elif "password" not in data:
        return Response({
            "status_code": 400,
            'msg': "请输入password"
        })
    elif data["username"] == "" or data["username"] == " ":
        return Response({
            "status_code": 400,
            'msg': "username不能为空"
        })
    elif data["password"] == "" or data["password"] == " ":
        return Response({
            "status_code": 400,
            'msg': "password不能为空"
        })
    else:
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({
                "status_code": 400,
                'msg': "该用户不存在"
            })
        password = data['password']
        passwdcheck = check_password(password, user.password)
        if passwdcheck:
            return Response({
                "status_code": 200,
                'msg': "登录成功"
            })
        else:
            return Response({
                "status_code": 400,
                'msg': "密码错误"
            })


# 登录接口-get
@csrf_exempt
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def login_get(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "status_code": 400,
            'msg': "用户不存在"
        })
    passwdcheck = check_password(password, user.password)
    if passwdcheck:
        return Response({
            "status_code":200,
            'msg': "登录成功"
        })
    else:
        return Response({
            "status_code": 400,
            'msg': "密码错误"
        })
# 注册接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    """
    参数示例：
    data = {
        'username': "luoshiling18",
        'password': admin12345,
        'email': "15901304866@163.com",
    }
    :param request:
    :return:
    """
    data = json.loads(request.body)
    if "username" not in data:
        return Response({
            "status_code": 400,
            'msg': "请输入username"
        })
    elif "password" not in data:
        return Response({
            "status_code": 400,
            'msg': "请输入password"
        })
    elif "email" not in data:
        return Response({
            "status_code": 400,
            'msg': "请输入email"
        })
    elif data["username"] == "" or data["username"] == " ":
        return Response({
            "status_code": 400,
            'msg': "username不能为空"
        })
    elif data["password"] == "" or data["password"] == " ":
        return Response({
            "status_code": 400,
            'msg': "password不能为空"
        })
    elif data["email"] == "" or data["email"] == " ":
        return Response({
            "status_code": 400,
            'msg': "email不能为空"
        })
    elif User.objects.filter(username=data['username']):
        return Response({
            "status_code": 400,
            'msg': "该用户已注册"
        })
    elif User.objects.filter(email=data['email']):
        return Response({
            "status_code": 400,
            'msg': "该邮箱已注册"
        })
    else:
        user = User(email=data['email'],
                    password=make_password(data['password']),
                    username=data['username'])
        user.save()
        return Response({
            "status_code": 200,
            'msg': "注册成功"
        })


# 数据库检查字段  目前没用
def is_fields_error(_model, fields, ex_fields):
    from django.db import models
    """
    @note 检查相应的_model里是否含有params所有key，若为否，则返回第一个遇到的不在_model里的key和False
    否则，返回为空True与空
    :param _model: fields:待检查字段  ex_fields:不在检查范围内的字段，比如外键
    :param params:
    :return: True,'' / False, key
    """
    if ex_fields:
        for i in ex_fields:
            if i in fields:
                fields.remove(i)

    if not (issubclass(_model, models.Model) and isinstance(fields, (list, tuple))):
        return False, u'参数有误'

    all_fields = list(_model._meta.get_fields())
    print(all_fields)
    for key in fields:
        if key not in all_fields:
            return False, key
    return True, ''


# 添加房源接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def add_lodgeinfo(request):
    """
    参数示例：
    info_dict = {"dayprice":3,
    #              "estate":"valid",
    #              "minday":1,
    #              "maxday":2,
    #              "tel":"15901304864",
    #              "remarks":"",
    #              "address_id":"124253424342",
    #              "image_md5":"sfdgwet4husf98fwiuhfsjkdhwh"
    #             }
    :param request:
    :return:
    """
    info_dict = json.loads(request.body)
    # _flag, func_r = is_fields_error(lodgeunitinfo, list(info_dict.keys()), ex_fields=['id','create_time','update_time'])
    # if not _flag:
    #     print("触发", func_r)
    # else:
    #     print("没触发", func_r)
    if "dayprice" not in info_dict:
        return Response({"status_code": 400, "msg": "dayprice必传"})
    elif "estate" not in info_dict:
        return Response({"status_code": 400, "msg": "estate必传"})
    elif "minday" not in info_dict:
        return Response({"status_code": 400, "msg": "minday必传"})
    elif "maxday" not in info_dict:
        return Response({"status_code": 400, "msg": "maxday必传"})
    elif "tel" not in info_dict:
        return Response({"status_code": 400, "msg": "tel必传"})
    elif "address_id" not in info_dict:
        return Response({"status_code": 400, "msg": "address_id必传"})
    elif "image_md5" not in info_dict:
        return Response({"status_code": 400, "msg": "image_md5必传"})
    elif info_dict["dayprice"] == "" or info_dict["dayprice"] == " ":
        return Response({"status_code": 400, "msg": "dayprice不能为空"})
    elif info_dict["estate"] == "" or info_dict["estate"] == " ":
        return Response({"status_code": 400, "msg": "estate不能为空"})
    elif info_dict["minday"] == "" or info_dict["minday"] == " ":
        return Response({"status_code": 400, "msg": "minday"})
    elif info_dict["maxday"] == "" or info_dict["maxday"] == " ":
        return Response({"status_code": 400, "msg": "maxday不能为空"})
    elif info_dict["tel"] == "" or info_dict["tel"] == " ":
        return Response({"status_code": 400, "msg": "tel不能为空"})
    elif info_dict["address_id"] == "" or info_dict["address_id"] == " ":
        return Response({"status_code": 400, "msg": "address_id不能为空"})
    elif info_dict["image_md5"] == "" or info_dict["image_md5"] == " ":
        return Response({"status_code": 400, "msg": "image_md5不能为空"})
    elif info_dict["estate"] != "valid" and info_dict["estate"] != "deleted":
        return Response({"status_code": 400, "msg": "estate必须为 valid或deleted"})
    elif type(info_dict["dayprice"]) != type(1):
        return Response({"status_code": 400, "msg": "dayprice必须是int"})
    elif type(info_dict["minday"]) != type(1):
        return Response({"status_code": 400, "msg": "minday必须是int"})
    elif type(info_dict["maxday"]) != type(1):
        return Response({"status_code": 400, "msg": "maxday必须是int"})
    elif info_dict["minday"] == info_dict["maxday"]:
        return Response({"status_code": 400, "msg": "minday 不能等于 maxday"})
    elif info_dict["minday"] > info_dict["maxday"]:
        return Response({"status_code": 400, "msg": "minday 不能大于 maxday"})
    else:
        try:
            lodgeunitinfo.objects.create(**info_dict)
            return Response({"status_code": 200, "msg": "房源添加成功"})
        except Exception:
            exception_info = sys.exc_info()
            # print(exception_info[0], type(exception_info[0]))
            # print(exception_info[1], type(exception_info[1]))
            #return Response({"status_code": 400, "msg":str(exception_info[0]) + ":" + str(exception_info[1])})
            return Response({"status_code": 400, "msg": "房源添加失败"})


# 订单接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def create_order(request):#这个是创建订单接口，request接受请求实例，里面包含
                            #本次请求所有信息；
    """
    参数示例：
    order_info = {
    #     "luid":1,
    #     "guestnum":2,
    #     "checkinday":"2019-01-03",
    #     "checkoutday":"2019-01-04"
    # }
    :param request:
    :return:
    """
    data = json.loads(request.body)#获取post-body请求体，可以忽略
    query = request.GET.get("sign")#这里获取url中的sign值，
    if  not query:#做个非空判断
        return Response({"status_code": 400, "msg": "sign必传"})
    str_md5 = hashlib.md5(b'admin').hexdigest()#这步是使用约定好的字符串
    #print("str_md5:",str_md5)             # admin md5加密生成str_md5
    if str_md5 != query:#然后把生成的str_md5和请求传过来的sign值比较，如果
                        #相同，则验证通过，反之，不通过；我们看下生成的
                        # str_md5长什么样；打印一下
                        #str_md5: 21232f297a57a5a743894a0e4a801fc3
                        #是这个东西，我们把这个字符串放到请求里面试一下
        return Response({"status_code": 400, "msg": "验签失败"})
    if "luid" not in data:
        return Response({"status_code": 400, "msg": "luid必传"})
    elif "guestNum" not in data:
        return Response({"status_code": 400, "msg": "guestNum必传"})
    elif "checkInDate" not in data:
        return Response({"status_code": 400, "msg": "checkInDate必传"})
    elif "checkOutDate" not in data:
        return Response({"status_code": 400, "msg": "checkOutDate必传"})
    elif data["luid"] == "" or data["luid"] == " ":
        return Response({"status_code": 400, "msg": "luid不能为空"})
    elif data["guestNum"] == "" or data["guestNum"] == " ":
        return Response({"status_code": 400, "msg": "guestNum不能为空"})
    elif data["checkInDate"] == "" or data["checkInDate"] == " ":
        return Response({"status_code": 400, "msg": "checkInDate不能为空"})
    elif data["checkOutDate"] == "" or data["checkOutDate"] == " ":
        return Response({"status_code": 400, "msg": "checkOutDate不能为空"})
    else:
        #  房源存在校验
        luId = data['luId']
        daynum = datetime.datetime.strptime(data['checkOutDate'], '%Y-%m-%d') - datetime.datetime.strptime(data['checkInDate'],'%Y-%m-%d')
        id_list = []
        lodgeinfo = lodgeunitinfo.objects.filter(id=str(luId))
        dayprice = 0
        allowdays = 0
        for i in lodgeinfo:
            dayprice = i.dayprice
            allowdays = i.maxday - i.minday
        for i in lodgeunitinfo.objects.values('id'):
            id_list.append(i['id'])
        if luId not in id_list:
            return Response({"status_code": 400, "msg": "房源" + str(luId) + "不存在"})
        elif daynum.days < 1:
            return Response({"status_code": 400, "msg": "入住时间不能晚于离开时间"})
        elif daynum.days > allowdays:
            return Response({"status_code": 400, "msg": "入住时间段不能长于最长时间"})
        else:
            totalprice = int(daynum.days) * dayprice
            #print("日价", dayprice, "天数", daynum.days)
            data["totalprice"] = totalprice
            order.objects.create(**data)
            return Response({"status_code": 200, "msg": "创建订单成功"})


# 支付回调接口--示例
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def payback_order(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='done')
    except Exception:
        return Response({"status_code": 400, "msg": "订单回调更新失败"})
    return Response({"status_code": 200, "msg": "支付成功"})


# 支付第三方接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def others_pay_order(request):
    data = json.loads(request.body)
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




# 支付接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def pay_order(request):
    """
    参数示例：
    pay_order_info = {
        "order_id": 1,
        "luid": 1
    }
    :param request:
    :return:
    """
    data = json.loads(request.body)
    if "order_id" not in data:
        return Response({"status_code": 400, "msg": "order_id必传"})
    elif "luid" not in data:
        return Response({"status_code": 400, "msg": "luid必传"})
    elif data["order_id"] =="" or data["luid"] == " ":
        return Response({"status_code": 400, "msg": "order_id不能为空"})
    elif data["luid"] =="" or data["luid"] == " ":
        return Response({"status_code": 400, "msg": "luid不能为空"})
    else:
        #  订单参数检查
        order_id = data['order_id']
        luid = data['luid']
        try:
            orderinfo = order.objects.filter(id=str(order_id))
        except Exception:
            return Response({"status_code": 400, "msg": "订单不存在"})
        try:
            luinfo = lodgeunitinfo.objects.filter(id=str(luid))
        except Exception:
            return Response({"status_code": 400, "msg": "房源不存在"})
        for i in orderinfo:
            if luid == i.luid:
                if i.estate == 'valid':
                    for j in luinfo:
                        if j.estate == 'valid':
                            coo_other_pay = threading.Thread(target=others_pay_order_true, kwargs=({"order_id": order_id, "totalprice": i.totalprice, "estate": "yes"}))
                            coo_other_pay.start()
                            return Response({"status_code": 200, "msg": "第三方支付接口调用成功，支付成功"})
                        else:
                            return Response({"status_code": 400, "msg": "房源已下线或已被预订"})
                else:
                    return Response({"status_code": 400, "msg": "订单已失效"})
            else:
                return Response({"status_code": 400, "msg": "订单与房源不匹配"})


@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def cancel_order(request):
    data = json.loads(request.body)
    if "order_id" not in data:
        return Response({"status_code": 400, "msg": "order_id必传"})
    elif data["order_id"] == "" or data["order_id"] == " ":
        return Response({"status_code": 400, "msg": "order_id不能为空"})
    else:
        order_id = data['order_id']
        try:
            orderinfo = order.objects.filter(id=str(order_id))
        except Exception:
            return Response({"status_code": 400, "msg": "订单不存在"})
        for i in orderinfo:
            if i.estate == 'done':
                return Response({"status_code": 400, "msg": "订单已完成，不能取消"})
            elif i.estate == "valid":
                orderinfo.update(estate="cancel")
                return Response({"status_code": 200, "msg": "订单取消成功"})
            else:
                return Response({"status_code": 400, "msg": "订单已被取消或订单异常"})


@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def pushAPIInfo(request):
    data = json.loads(request.body)
    print(data)
    print(type(data))
    return Response({"status_code": 200, "msg": "信息接收成功"})


#获取房源信息接口
@csrf_exempt
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def get_lodgeunitInfo(request):
    """
    :param request:offset,limit,luId,type(list/all) 参数可选
    :return:
    """
    offset = request.GET.get("offset")
    if not offset:
        offset = 0
    limit = request.GET.get("limit")
    if not limit:
        limit = 10
    luId = request.GET.get("luId")
    type = request.GET.get("type")
    if not type:
        type = "all"
    estate = request.GET.get("estate")
    try:
        offset = int(offset)
    except Exception:
        return Response({"status_code": 400, "msg": "offset必须为整数"})
    try:
        limit = int(limit)
    except Exception:
        return Response({"status_code": 400, "msg": "limit必须为整数"})
    if offset < 0:
        return Response({"status_code": 400, "msg": "offset不能小于0"})
    if limit < 0:
        return Response({"status_code": 400, "msg": "limit不能小于0"})
    if luId:
        try:
            lodgeUnitInfo = lodgeunitinfo.objects.filter(id=luId)
        except Exception:
            return Response({"status_code": 400, "msg": "luId不存在"})
    else:
        lodgeUnitInfo = lodgeunitinfo.objects.filter(estate='valid')[offset:limit]
    infoData = {"status_code": 200,
                "content": []}
    if type == "list":
        luIdList = lodgeUnitInfo.values_list('id')
        infoData["length"] = len(luIdList)
        infoData["content"] = luIdList
        return Response(infoData)
    elif type == "all":
        luIdDataList = lodgeUnitInfo.values()
        infoData["length"] = len(luIdDataList)
        infoData["content"] = luIdDataList
        return Response(infoData)

#获取房源信息接口
@csrf_exempt
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def get_ordertInfo(request):
    """
        :param request:offset,limit,luId,type(list/all),estate(valid,done,cancel) 参数可选
        :return:
        """
    offset = request.GET.get("offset")
    if not offset:
        offset = 0
    limit = request.GET.get("limit")
    if not limit:
        limit = 10
    orderId = request.GET.get("orderId")
    print(orderId)
    type = request.GET.get("type")
    if not type:
        type = "all"
    estate = request.GET.get("estate")
    if not estate:
        estate = "valid"
    try:
        offset = int(offset)
    except Exception:
        return Response({"status_code": 400, "msg": "offset必须为整数"})
    try:
        limit = int(limit)
    except Exception:
        return Response({"status_code": 400, "msg": "limit必须为整数"})
    if offset < 0:
        return Response({"status_code": 400, "msg": "offset不能小于0"})
    if limit < 0:
        return Response({"status_code": 400, "msg": "limit不能小于0"})
    if orderId:
        #print(order)
        try:
            orderInfo = order.objects.filter(id=orderId)
        except Exception:
            return Response({"status_code": 400, "msg": "orderId不存在"})
    else:
        orderInfo = order.objects.filter(estate=estate)[offset:limit]
    infoData = {"status_code": 200,
                "content": []}
    if type == "list":
        orderIdList = orderInfo.values_list('id')
        infoData["length"] = len(orderIdList)
        infoData["content"] = orderIdList
        return Response(infoData)
    elif type == "all":
        orderIdDataList = orderInfo.values()
        infoData["length"] = len(orderIdDataList)
        infoData["content"] = orderIdDataList
        return Response(infoData)



