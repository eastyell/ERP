# 模块名称：网关
# 创建日期：2020-6
# 最后修改日期：2020-6
# 作者：Jason

"""
WSGI config for crm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

application = get_wsgi_application()
