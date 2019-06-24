import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'building_knowledge_stack_db',
        'USER': 'turkey',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
        # 'OPTIONS': {
        #     'init_command': 'SET CHARACTER SET utf8mb4',
        #     'charset': 'utf8mb4',
        # },
        'TEST': {
            'NAME': 'test_building_knowledge_stack_db',
            # 'CHARSET': 'utf8mb4',
        }
    }
}


# class MinprogramSettings:
#     APP_ID = 'wx1743dc274cf46871'
#     APP_SECRET = '648a7ae2cbf66aa7e48992d76f46e621'
#     LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session' \
#                 '?appid={}&secret={}&grant_type=authorization_code&js_code='.format(APP_ID, APP_SECRET)


class QiNiuSettings:
    ACCESS_KEY = 'YU8-GbpmWJ_8UEdBc7VTv4n_eku3zlgoHuUI2l9D'
    SECRET_KEY = 'Mkms7UphbEH4sWdkWoEnqk0PCjD3V84rIZ3EuL_H'
    BUCKET_NAME_DICT = {
        'image': 'img3-workspace',
        'video': 'img-workspace'
    }
    BUCKET_DOMAIN_DICT = {
        'image': 'http://lhxq.top/',
        'video': 'http://video.lhxq.top/'
    }


class AliYunSMS:
    ACCESS_KEY_ID = "LTAILW2rTviNT3NS"
    ACCESS_KEY_SECRET = "exfqW4cxb7QrE3CExWqF4B7TKzifxr"
    SMS_TEMPLATE_NAME = '邯郸鼎典'
    SMS_TEMPLATE_ID = 'SMS_160861562'


class AlipaySettings:
    _root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_ID = '2019061765593239'
    APP_PRIVATE_KEY = os.path.join(_root_dir, 'config/alipay/test_app_private.txt')
    ALIPAY_PUBLIC_KEY = os.path.join(_root_dir, 'config/alipay/test_alipay_public_key_sha256.txt')
    VIRTUAL_SERVICE_NOTIFY_URI = 'https://tm.lhxq.top/application/alipay_notify/'


class WeChatPaySettings:
    WEIXIN_APP_ID = 'wx502707dff6e8ce6c'
    WEIXIN_APP_SECRET = '7968e86926fc96525807d0256edaadff'
    WEIXIN_MCH_ID = '1527643731'
    WEIXIN_MCH_KEY = 'handanxiaohongniang1234567890000'
    WEIXIN_NOTIFY_URL = 'https://tm.lhxq.top/application/wechatpay_notify/'