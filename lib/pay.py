import string
from datetime import datetime
from random import choice

from alipay import AliPay
from weixin import WeixinPay

from server.settings import AlipaySettings, WeChatPaySettings


def gen_union_trade_no(pay_type=1):
    """
    生成内部订单号
    格式：
    {pay_type}{20190119161237}{0001}
    :param pay_type: 1: 支付宝， 2：微信
    :return:
    """
    create_time = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join([choice(string.digits) for _ in range(4)])
    return '{pay_type}{create_time}{random_str}'.format(pay_type=pay_type,
                                                        create_time=create_time,
                                                        random_str=random_str
                                                        )


alipay_serve = AliPay(
    appid=AlipaySettings.APP_ID,
    app_notify_url=None,  # 默认回调url
    app_private_key_path=AlipaySettings.APP_PRIVATE_KEY,
    alipay_public_key_path=AlipaySettings.ALIPAY_PUBLIC_KEY,
    sign_type="RSA2",
    debug=False
)

# alipay_serve = None

wechatpay_serve = WeixinPay(
    app_id=WeChatPaySettings.WEIXIN_APP_ID,
    mch_id=WeChatPaySettings.WEIXIN_MCH_ID,
    mch_key=WeChatPaySettings.WEIXIN_MCH_KEY,
    notify_url=WeChatPaySettings.WEIXIN_NOTIFY_URL
)