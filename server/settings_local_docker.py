DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'building_knowledge_stack_db',
        'USER': 'building_user',
        'PASSWORD': 'password@123/',
        'HOST': 'db',
        'PORT': 5432,
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

