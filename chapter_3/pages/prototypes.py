import os
import sys
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read("settings.ini")

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, config_parser.get("django", "TEMPLATE_DIRS")),
]
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, config_parser.get("django", "STATICFILES_DIRS")),
)

DEBUG = True if config_parser.get("django", "DEBUG") == "True" else False
ALLOWED_HOSTS = config_parser.get("django", "ALLOWED_HOSTS").split(",")

settings.configure(
    DEBUG=True,
    SECRET_KEY='b0mqvak1p2sqm6p#+8o8fyxf+ox(le)8&jh_5^sxa!=7!+wxj0',
    ROOT_URLCONF='sitebuilder.urls',
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'sitebuilder'
    ),
    STATIC_URL='/static/',
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, 'pages'),
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'sitebuilder', 'templates')],
    }],
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
