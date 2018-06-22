# Stdlib imports
import datetime
# Core Django imports
from django.utils import timezone
# Third-party app imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
# Imports from your apps
from customers.models import Customer
from customers.serializers import CustomerPaymentResponseSerializer
from orders.models import Order
from .methods import payment_qr_code_with_offline_order, payment_with_balance, payment_with_wechat_online_order
from wechatpay.methods import trans_xml_to_dict, trans_dict_to_xml
from wechatpay.methods import wechat_pay_query, wechat_pay_cancel
from alipayment.methods import alipay_trade_query, alipay_trade_cancel


@permission_classes((AllowAny, ))
class GetTencentNotifyView(APIView):
    def post(self, request):
        msg = request.text.encode('ISO-8859-1').decode('utf-8')
        res = trans_xml_to_dict(msg)

        if res.get('return_code') == 'SUCCESS':
            if res.get('result_code') == 'SUCCESS':
                trade_no = res.get('out_trade_no')
                order = Order.objects.get(tradeNo=trade_no)
                wuser = order.userID
                order.status = 3
                wuser.point = wuser.point + order.payPrice * 100
                order.paymentSN = res.get('transaction_id')
                order.payTime = timezone.now()
                order.paymentMethod = 'wechatpay'
                order.save()
            else:
                error_code = res.get('err_code')
                error_mes = res.get('err_code_des')
                print(error_code, error_mes)
        else:
            error_mes = res.get('return_msg')
            print(error_mes)

        res = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK',
        }
        res_xml = trans_dict_to_xml(res)
        return Response(res_xml, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class GetAlipayNotifyView(APIView):
    def post(self, request):
        if request.get('trade_status') == '交易支付成功':
            tradeNo = request.get('out_trade_no')
            order = Order.objects.get(tradeNo=tradeNo)
            wuser = order.userID
            order.status = 3
            wuser.point = wuser.point + order.payPrice * 100
            order.paymentSN = request.get('trade_no')
            order.payTime = timezone.now()
            order.paymentMethod = 'Alipay_Pay_In_Store'
            order.save()
        else:
            trade_status = request.get('trade_status')
            print(trade_status)

        return Response('SUCCESS', status=status.HTTP_200_OK)


class PayOrderPreProcess(APIView):
    """
    :return:
    orderMethod == 0 (online pay)
    SUCCESS
    {
        'timeStamp': timestamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'MD5',
        'paySign': paysign,
        'tradeNo': out_trade_no,
        'status': 1 # pay by ali/wechat
    }
    FAILED
    {
        'status' : 404
    }
    -------------------------------------
    orderMethod == 1 (offline pay)
    SUCCESS
    {
        'AliPayQRcodeUrl': timestamp,
        'WechatPayQRcodeUrl': nonce_str,
        'status': 1 # pay by ali/wechat
    }
    FAILED
    {
        'status' : 404
    }
    -------------------------------------
    balance payment (balance pay)
    {
        'status' : 2, # pay with balance
        'balance': 'userBalance',
    }
    """
    def post(self, request):
        # get data from request
        order_method = request.data.get('order_method')
        user_id = request.data.get('user_id')
        trade_no = request.data.get('trade_no')

        # get userInfo from database
        wuser = Customer.objects.get(pk=user_id)
        open_id = wuser.openid

        # get orderInfo from database
        order = Order.objects.get(tradeNo=trade_no)
        # calculate the pay money and determin the method of payments
        if order.payPrice > 0:  # user Alipay or WechatPay
            wuser.balance = 0
            wuser.save()
            if order_method == 0:  # user WechatPay within miniApp
                res = payment_with_wechat_online_order(trade_no, open_id)
                res['pay_method'] = 1
                return Response(res, status=status.HTTP_200_OK)
            if order_method == 1:  # offline order
                res = payment_qr_code_with_offline_order(trade_no, open_id)
                return Response(res, status=status.HTTP_200_OK)
        else:
            # complete pay if balance is enough to pay
            res = payment_with_balance(trade_no, order_method)
            res['pay_method'] = 2
            return Response(res, status=status.HTTP_200_OK)


class PaySuccessView(APIView):
    """
    When wechatPay success, request for this Api,it will renew the order and user info, also query the tencent server to ensure the payment
    miniApp-cart/index.js & balance.js & order.js & detail.js

    Parameters:
        id - user uuid
        tradeNo - the tradeNo of selected order

    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):
        order = Order.objects.get(tradeNo=request.data.get('trade_no'))
        wuser = Customer.objects.get(id=request.data.get('user_id'))
        querydata = wechat_pay_query(request.data.get('trade_no'))

        if querydata.get('status') == 200:
            order.status = 1
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = querydata.get('transaction_id')
            order.payTime = timezone.now()
            order.paymentMethod = 'Wechat Pay'
            order.save()

        if querydata.get('status') == 400:
            return Response(400, status=status.HTTP_200_OK)

        wuser.save()
        serializer = CustomerPaymentResponseSerializer(wuser)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OfflinePayQueryView(APIView):
    """
    Request for this Api,it will query the tencent & alipay server to ensure the payment status(default request every 2s)

    Parameters:
        user_id - user uuid
        trade_no - the trade no of payment


    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):
        out_trade_no = request.data.get('trade_no')
        order = Order.objects.get(tradeNo=out_trade_no)
        wuser = Customer.objects.get(id=request.data.get('user_id'))

        # query data from alipay and wechat server
        wechatquerydata = wechat_pay_query(out_trade_no)
        alipayquerydata = alipay_trade_query(out_trade_no)

        print(wechatquerydata)
        print(alipayquerydata)

        is_alipay_order_paid = False
        is_wechatpay_order_paid = False

        if wechatquerydata.get('status') == 200:
            order.status = 3
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = wechatquerydata.get('transaction_id')
            order.payTime = timezone.now()
            order.paymentMethod = 'Wechat Pay'
            order.save()
            is_wechatpay_order_paid = True

        if alipayquerydata.get('status') == 200:
            order.status = 3
            wuser.point = wuser.point + order.payPrice*100
            order.paymentSN = alipayquerydata.get('trade_no')
            order.payTime = timezone.now()
            order.paymentMethod = 'Alipay Pay'
            order.save()
            is_alipay_order_paid = True

        wuser.save()
        if is_wechatpay_order_paid:
            serializer = CustomerPaymentResponseSerializer(wuser)
            alipay_trade_cancel(out_trade_no)
            res = serializer.data
            res['msg'] = 'Pay Success: WechatPay'
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_alipay_order_paid:
            serializer = CustomerPaymentResponseSerializer(wuser)
            wechat_pay_cancel(out_trade_no)
            res = serializer.data
            res['msg'] = 'Pay Success: Alipay'
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                'status' : 'Not paid or Close',
                'Alipay' : alipayquerydata,
                'Wechat' : wechatquerydata,
            }
            return Response(res, status=status.HTTP_204_NO_CONTENT)


class OfflinePayCancelView(APIView):
    """
    Request for this Api,it will sent the request to the tencent & alipay server to cancel the payment which is timeout

    Parameters:
        trade_no - the trade no of payment
        user_id - user uuid


    Returns:
      id - user uuid
      point -
      level -
      balance -

    Raises:
    """
    def post(self, request):
        out_trade_no = request.data.get('trade_no')
        order = Order.objects.get(tradeNo=out_trade_no)
        wuser = Customer.objects.get(id=request.data.get('user_id'))

        wechat_res = wechat_pay_cancel(out_trade_no)
        alipay_res = alipay_trade_cancel(out_trade_no)

        if wechat_res.get('status') == 200 & alipay_res.get('status') == 200:
            order.status = 6
            order.cancelTime = timezone.now()
            order.paymentMethod = 'Cancel'
            order.save()
            wuser.balance = order.balanceUse
            wuser.save()
            serializer = CustomerPaymentResponseSerializer(wuser)
            res = serializer.data
            res['msg'] = 'Order Success Cancel '
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response('Error', status=status.HTTP_409_CONFLICT)