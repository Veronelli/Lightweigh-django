import sys
from django.urls import re_path
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('settings.ini')

DEBUG = True if config_parser.get('django', 'DEBUG') == 'True' else False

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=config_parser.get('django', 'SECRET_KEY'),
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

application = get_wsgi_application()

def index(request):
    return HttpResponse('Hello World')


urlpatterns = (
    re_path(r'^$', index),
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
