import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'users',
    'game',
]

# Channels
ASGI_APPLICATION = 'gobang.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

DEBUG = True

# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 添加这个设置

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 添加这个目录
        'APP_DIRS': True,  # 确保设置为 True
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 数据库配置（这里使用默认的SQLite）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# 中间件配置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 必须在这里
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 必须在这里
    'django.contrib.messages.middleware.MessageMiddleware',  # 必须在这里
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 设置允许的主机
ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# 在settings.py文件中
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 根URL配置
ROOT_URLCONF = 'gobang.urls'

# 设置密钥
SECRET_KEY = 'your_secret_key_here'
