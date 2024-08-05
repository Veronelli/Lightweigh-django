from io import BytesIO
import sys
from django import forms
from django.urls import re_path
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from configparser import ConfigParser
from django.core.cache import cache
from PIL import Image, ImageDraw, ImageFont

config_parser = ConfigParser()
config_parser.read('settings.ini')

DEBUG = True if config_parser.get('django', 'DEBUG') == 'True' else False
ALLOWED_HOSTS = config_parser.get('django', 'ALLOWED_HOSTS').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=config_parser.get('django', 'SECRET_KEY'),
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

application = get_wsgi_application()


def index(request: HttpRequest) -> HttpResponse:
    """
    Returns a simple 'Hello World' response.
    :param request: HttpRequest
    :return: HttpResponse
    """
    return HttpResponse('Hello World')


class ImageForm(forms.Form):
    """Form to validate request size values"""
    height = forms.IntegerField(min_value=1, max_value=4096)
    width = forms.IntegerField(min_value=1, max_value=4096)
    
    def generate(self, image_format='PNG'):
        """
        Generates a placeholder image.
        :param image_fomat: str
        :return: Image
        """
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        print(content)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textbbox = draw.textbbox(
                [width/2, height/2], text, font_size=100)
            text_height = textbbox[3] - textbbox[1]
            
            text_width = textbbox[2] - textbbox[0]
            if text_width < width and text_height < height:
                texttop = (height - text_height) // 2
                textleft = (width - text_width) // 2
                font = ImageFont.FreeTypeFont(
                    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                    size=100)
                draw.text(
                    (textleft, texttop),
                    text,
                    fill=(255, 255, 255),
                    font=font
                )
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60*60)
        return content


def placeholder(request: HttpRequest, width: str, height: str):
    """
    Returns a placeholder response.
    :param request: HttpRequest
    :param width: int
    :param height: int
    :return: HttpResponse
    """
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')

    return HttpResponseBadRequest('Invalid Image Request')

urlpatterns = (
    re_path(r'^$', index),
    re_path(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder)
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
