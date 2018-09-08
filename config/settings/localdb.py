from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': r'C:\Users\leonh\workspace\PhotoPaul\db.sqlite3',
    }
}

ALLOWED_HOSTS = ['localhost']

MEDIA_URL = '/media/'
MEDIA_ROOT = r'C:\Users\leonh\workspace\PhotoPaul' + '\\'

SECRET_KEY = '8nl+o)*dgfzo2v0z6@90zc2l9e&)-ig(a5!_64=)p=#n=@uk9p'
INSTALLED_APPS = tuple(x for x in INSTALLED_APPS if x != 'imprint')
