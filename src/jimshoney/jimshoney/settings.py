"""
Django settings for jimshoney project.

Generated by 'django-admin startproject' using Django 2.0.7.

"""

import logging
import os
from django.utils.translation import ugettext_lazy as _
from oscar import OSCAR_MAIN_TEMPLATE_DIR, get_core_apps
from oscar.defaults import *
from gramedia.common.env import EnvConfig
from .base_celery import *

env_prefix = os.getenv('APP_ENV_PREFIX', 'JIM')

env = EnvConfig(env_prefix)

SITE_ID = 1

WSGI_APPLICATION = 'jimshoney.wsgi.application'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^b46w^zsxhrthkq2p7ty1dt5zov%4@eq@j8e%f(ki_#2rnbp%-d"
OSCAR_GOOGLE_ANALYTICS_ID = env.string('GTM', 'GTM-ND5F5RB')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.boolean('DEBUG', True)
THUMBNAIL_DEBUG = DEBUG
SESSION_COOKIE_SECURE = not DEBUG
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CONN_MAX_AGE = 0
    SECURE_HSTS_SECONDS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': env.string('MEMCACHE_HOST', '127.0.0.1') + ':11211',
        }
    }

INSTALLED_APPS = [
     'debug_toolbar',
     'apps.user',
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'django.contrib.flatpages',
     'django_extensions',
     'widget_tweaks',
     'celerybeat_status',
     'compressor',
     'apps.campaign',
     'apps.dashboard.campaign',
     'apps.dashboard.destination_ranges',
     'apps.partner_api',
     'apps',
     'meta'
 ] + get_core_apps([
    'apps.address',
    'apps.basket',
    'apps.customer',
    'apps.catalogue',
    'apps.checkout',
    'apps.dashboard.catalogue',
    'apps.dashboard.orders',
    'apps.dashboard.users',
    'apps.dashboard.ranges',
    'apps.dashboard.reports',
    'apps.dashboard.offers',
    'apps.dashboard.vouchers',
    'apps.dashboard',
    'apps.order',
    'apps.offer',
    'apps.partner',
    'apps.payment',
    'apps.search',
    'apps.shipping',
    'apps.voucher'
])
INTERNAL_IPS = [
    '127.0.0.1',
    '.gramedia.io',
]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.gramedia.io',
    '.jimshoneyofficial.com',
]

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, '../../fixtures'),
)

# Application definition


SITE_ID = 1

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'jimshoney.urls'

HTML_MINIFY = False
EXCLUDE_FROM_MINIFYING = ('^dashboard/',)

# Request ID log related
LOG_REQUEST_ID_HEADER = env.string('HTTP_X_REQUEST_ID', 'HTTP_X_REQUEST_ID')
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = env.boolean('GENERATE_REQ_ID', True)
REQUEST_ID_RESPONSE_HEADER = env.string('RESPONSE_REQ_ID', "RESPONSE_REQ_ID")
LOG_REQUESTS = env.boolean('LOG_REQUESTS', True)
ENVIRONMENT = env.string('ENVIRONMENT', 'staging')
GRAYLOG_HOST = env.string('GRAYLOG_HOST', 'logs.gramedia.io')
GRAYLOG_PORT = env.int('GRAYLOG_PORT', 13302)
GRAYLOG_HANDLER = env.string('GRAYLOG_HANDLER', 'graypy.GELFTcpHandler')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'app': {
            'class': 'logging.handlers.RotatingFileHandler',
            'encoding': 'utf8',
            'filename': os.path.join(BASE_DIR, '../../logs', 'app.log'),
            'formatter': 'standard',
            'level': logging.DEBUG,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 10,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'graylog': {
            'level': logging.DEBUG if DEBUG else logging.INFO,
            'class': GRAYLOG_HANDLER,
            'host': GRAYLOG_HOST,
            'port': GRAYLOG_PORT,
            'filters': ['request_id', 'request_meta', 'user_filter', 'static_fields', 'request_filter'],
            'formatter': 'json'
        },
    },
    'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse', },
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue', },
        'user_filter': {'()': 'utils.logging.UserFilter'},
        'static_fields': {
            '()': 'utils.logging.StaticFieldFilter',
            'fields': {
                'environment': ENVIRONMENT,  # can be overridden in local_settings.py
                'application': WSGI_APPLICATION
            },
        },
        'request_filter': {
            '()': 'utils.logging.RequestFilter'
        },
        'request_id': {
            '()': 'utils.logging.RequestIDFilter'
        },
        'request_meta': {
            '()': 'utils.logging.RequestMetaFilter'
        }
    },
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
        'standard': {
            'format': f"[{'DEV' if DEBUG else 'PROD'}]"
            f"JIMSHONEY.COM E-COMMERCE [%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'verbose': {
            'format': '%(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'loggers': {
        'jimshoney': {
            'handlers': ['app', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'oscar.core': {
            'handlers': ['app', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

ADMINS = [
    ('jimshoney error', env.string('DEBUG_EMAIL', 'error.jimshoney@staff.gramedia.com')),
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
                'jimshoney.context_processors.global_settings',
            ],
        },
    },
]

DATABASES = {
    'default': env.django_db('DB_URI_PASS', 'postgresql://jimshoney:p@ssw0rd24@localhost:5432/jimshoney')
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://' + env.string('SOLR_HOST', '127.0.0.1') + ':8983/solr/jimshoney',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'ADMIN_URL': 'http://' + env.string('SOLR_HOST', '127.0.0.1') + ':8983/solr/admin/cores'
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# AUTH_USER_MODEL = 'user.User'

LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

os.environ["LANGUAGE"] = 'id'

DATE_INPUT_FORMATS = ['%Y-%m-%d',  # '2006-10-25'
                      '%m/%d/%Y',  # '10/25/2006'
                      '%m/%d/%y',  # '10/25/06'
                      '%d/%m/%Y',  # '25/10/2006'
                      '%d/%B/%Y',  # '25/October/2006'
                      '%d-%m-%Y',  # '25-10-2006'
                      '%d-%B-%Y',  # '25-October-2006'
                      ]
DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M',  # '2006-10-25'
                          '%m/%d/%Y %H:%M',  # '10/25/2006'
                          '%m/%d/%y %H:%M',  # '10/25/06'
                          '%d/%m/%Y %H:%M',  # '25/10/2006'
                          '%d/%B/%Y %H:%M',  # '25/October/2006'
                          '%d-%m-%Y %H:%M',  # '25-10-2006'
                          '%d-%B-%Y %H:%M',  # '25-October-2006'
                          ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_ENABLED = not DEBUG
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_CSS_HASHING_METHOD = None
#
OSCAR_USE_LESS = DEBUG

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

OSCAR_SHOP_NAME = "Jims Honey"
OSCAR_SHOP_TAGLINE = "Jimshoney.com"
OSCAR_DEFAULT_CURRENCY = 'IDR'

ORDER_STATUS_PLACED = 'Placed'
ORDER_STATUS_CANCELED = 'Canceled'
ORDER_STATUS_PAID = 'Paid'
ORDER_STATUS_SHIPPED = 'Shipped'
ORDER_STATUS_COMPLETED = 'Completed'
ORDER_STATUS_REFUNDED = 'Refunded'

OSCAR_INITIAL_ORDER_STATUS = ORDER_STATUS_PLACED
OSCAR_INITIAL_LINE_STATUS = ORDER_STATUS_PLACED
OSCAR_ORDER_STATUS_PIPELINE = {
    ORDER_STATUS_PLACED: (ORDER_STATUS_PAID, ORDER_STATUS_CANCELED),
    ORDER_STATUS_PAID: (ORDER_STATUS_SHIPPED, ORDER_STATUS_CANCELED),
    ORDER_STATUS_SHIPPED: (ORDER_STATUS_COMPLETED,),
    ORDER_STATUS_CANCELED: (),
    ORDER_STATUS_COMPLETED: (ORDER_STATUS_REFUNDED,),
    ORDER_STATUS_REFUNDED: ()
}
OSCAR_LINE_STATUS_PIPELINE = {
    ORDER_STATUS_PLACED: (ORDER_STATUS_PAID, ORDER_STATUS_CANCELED),
    ORDER_STATUS_PAID: (ORDER_STATUS_SHIPPED, ORDER_STATUS_CANCELED),
    ORDER_STATUS_SHIPPED: (ORDER_STATUS_COMPLETED,),
    ORDER_STATUS_CANCELED: (),
    ORDER_STATUS_COMPLETED: (ORDER_STATUS_REFUNDED,),
    ORDER_STATUS_REFUNDED: ()
}
REPLACEMENT_STOCK_STATUS = (ORDER_STATUS_CANCELED, ORDER_STATUS_SHIPPED)

OSCAR_CURRENCY_FORMAT = {
    'IDR': {
        'format': u'Rp #,##0',
        'format_type': "accounting",
        'locale': 'de_DE',
    }
}
OSCAR_SEARCH_FACETS = {
    'fields': OrderedDict([
        ('attribute', {'name': 'Warna', 'field': 'attribute'}),
    ]),
    'queries': OrderedDict([
        ('price_range',
         {
             'name': 'Kisaran Harga',
             'field': 'price',
             'queries': [
                 ('0 to *', u'[0 TO *]')
             ]
         }),
    ]),
    'dynamic_queries_field_names': [field + '_exact' for field in ('price',)]
}
OSCAR_PRODUCTS_PER_PAGE = 12
OSCAR_REVIEWS_PER_PAGE = 5
OSCAR_SEND_REGISTRATION_EMAIL = False
OSCAR_FROM_EMAIL = 'no-reply@jimshoneyofficial.com'
OSCAR_TO_EMAIL = SERVER_EMAIL = 'admin@jimshoneyofficial.com'
OSCAR_ALLOW_ANON_REVIEWS = False
THUMBNAIL_SIZE = (150, 150)

LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Catalogue'),
        'icon': 'icon-sitemap',
        'children': [
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
            {
                'label': _('Brands'),
                'url_name': 'dashboard:brand-list',
            },
            {
                'label': _('Products'),
                'url_name': 'dashboard:catalogue-product-list',
            },
            {
                'label': 'Ranges',
                'url_name': 'dashboard:range-list',
            },
            {
                'label': 'Destination Ranges',
                'url_name': 'dashboard:destination-range-list',
            },
            {
                'label': _('Low stock alerts'),
                'url_name': 'dashboard:stock-alert-list',
            },
        ]
    },
    {
        'label': _('Fulfilment'),
        'icon': 'icon-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'dashboard:order-list',
            },
            {
                'label': _('Partners'),
                'url_name': 'dashboard:partner-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'dashboard:order-stats',
            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'dashboard:shipping-method-list',
            # },
        ]
    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'dashboard:user-alert-list',
            },
        ]
    },
    {
        'label': _('Campaign'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Banner'),
                'url_name': 'dashboard:banner-list',
            },
            {
                'label': _('Mini Banner'),
                'url_name': 'dashboard:banner-mini-list',
            },
            {
                'label': _('Endorsement'),
                'url_name': 'dashboard:endorsement-list',
            },

        ],
    },
    {
        'label': _('Offers'),
        'icon': 'icon-qrcode',
        'children': [
            {
                'label': _('Offers'),
                'url_name': 'dashboard:offer-list',
            },
            {
                'label': _('Vouchers'),
                'url_name': 'dashboard:voucher-list',
            },
            {
                'label': _('Voucher Sets'),
                'url_name': 'dashboard:voucher-set-list',
            },

        ],
    },
    {
        'label': _('Contents'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
            {
                'label': _('Reviews'),
                'url_name': 'dashboard:reviews-list',
            },
        ]
    },
    {
        'label': _('Reports'),
        'icon': 'icon-bar-chart',
        'url_name': 'dashboard:reports-index',
    },
]

BROKER_URL = env.string('RABBIT_CONN_PASS', 'amqp://guest:guest@127.0.0.1:5672//')

# Banner Mini Config
MAX_BANNER_MINI = 4
BANNER_MINI_PLACEHOLDER = {
    'image': 'image_not_founds.jpg',
    'title': 'default mini banner',
    'slug': 'default-mini-banner',
    'caption': 'default mini banner',
    'url': 'https://jimshoney.com/',
    'description': 'default mini banner',
    'published': True
}

# Jims Honey Social Media
SOCIAL_INSTAGRAM = 'https://www.instagram.com/jims_honey/'
SOCIAL_FACEBOOK = 'https://www.facebook.com/JIMSHONEYORI1/'
SOCIAL_TWITTER = 'https://twitter.com/JHFashion'
SOCIAL_YOUTUBE = 'https://www.youtube.com/channel/UCDmbLrCN7W2_pwrZDwg_e8Q'

NEW_FLAG_PRODUCT_PERIOD = 30  # days

OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1', 'province', 'regency_district', 'subdistrict',
                                 'village' 'postcode', 'country')

NEWSLETTER_FORM_INVALID_EMAIL_MESSAGE = 'Mohon masukkan alamat email yang valid.'
MAILCHIMP_API_KEY = env.string('MCHIMP_API_PASS', os.getenv('MCHIMP_API_PASS'))
MAILCHIMP_SUBSCRIBE_LIST_ID = env.string('MCHIMP_LIST_ID', os.getenv('MCHIMP_LIST_ID'))

EMAIL_HOST = env.string('EMAIL_HOST', 'smtp.mailtrap.io')
EMAIL_HOST_USER = env.string('EMAIL_HOST_USER', os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = env.string('EMAIL_HOST_PASS', os.getenv('EMAIL_HOST_PASS'))
EMAIL_PORT = env.string('EMAIL_PORT', '2525')
EMAIL_USE_TLS = env.boolean('EMAIL_USE_TLS', False)

USE_THOUSAND_SEPARATOR = True

KGX_API_URL = env.string('KGX_API_URL', 'https://test-api.kgx.co.id/api')
KGX_API_USERNAME = env.string('KGX_API_USERNAME', os.getenv('KGX_API_USERNAME'))
KGX_API_PASSWORD = env.string('KGX_API_PASS', os.getenv('KGX_API_PASS'))
KGX_ORIGIN_ZIP_CODE = env.string('KGX_ZIP_CODE', '14000')

IPAY_PAYMENT_URL = env.string('IPAY_URL', 'https://sandbox.ipay88.co.id/epayment/entry.asp')
IPAY_MERCHANT_CODE = env.string('IPAY_CODE', os.getenv('IPAY_CODE'))
IPAY_MERCHANT_KEY = env.string('IPAY_PASS', os.getenv('IPAY_PASS'))

SHIPPING_SENDER = {
    'name': 'CV. JIMSHONEY INDOTAMA',
    'mobile': '087878820660',
    'email': 'admin@jimshoneyofficial.com',
}

SHIPPING_ORIGIN = {
    'address': 'Jl. Setia No. 32, RT 1 /RW 3, Kedoya Selatan, Kebon Jeruk',
    'city': 'Jakarta Barat',
    'state': 'DKI Jakarta',
    'country': 'Indonesia',
    'postcode': '14000',
}

PAYMENT_AVAILABLE = [
    {
        'payment_method': 'virtual-account',
        'available': [
            'bca_va',
            'echannel',
            'bni_va',
            'permata_va',
        ]
    },
    {
        "payment_method": "credit-card",
        "available": [
            "credit_card"
        ]
    },
]

PAYMENT_LIST = {
    'BCA Virtual Account': {
        'name': 'BCA',
        'method': {
            'name': 'Bank Transfer Virtual Account',
            'value': 'virtual-account'
        },
        'imagePath': '/img/bank/bca.png',
        'message': '',
        'atm': [
            {
                'image': "img/thank-you/atm/atm-transfer.png",
                'description': '1. Pada ATM, Pilih opsi Transaksi Lainnya, lalu pilih opsi Transfer.'
            },
            {
                'image': "img/thank-you/atm/atm-virtual-account.png",
                'description': '2. Kemudian pilih opsi Ke Rekening BCA Virtual Account.'
            },
            {
                'image': "img/thank-you/atm/atm-input-number.png",
                'description': '3. Masukkan nomor rekening BCA Virtual Account.',

            },
            {
                'image': "img/thank-you/atm/atm-check.png",
                'description': '4. Periksa jumlah bayar, lalu selesaikan pembayaran.'
            },

        ],
        'internet': [
            {
                'image': "img/thank-you/internet-banking/internet-transfer.png",
                'description': '1. Login ke KlikBCA Individual, kemudian pilih opsi Transfer Dana.'
            },
            {
                'image': "img/thank-you/internet-banking/internet-virtual-account.png",
                'description': '2. Kemudian pilih opsi Transfer ke BCA Virtual Account.'
            },
            {
                'image': "img/thank-you/internet-banking/internet-number.png",
                'description': '3. Masukkan nomor rekening BCA Virtual Account.'
            },
            {
                'image': "img/thank-you/internet-banking/internet-check.png",
                'description': '4. Periksa jumlah bayar, lalu selesaikan pembayaran.'
            },

        ],
        'mobile': [
            {
                'image': "img/thank-you/mobile/mobile-1.png",
                'description': '1. Login ke BCA Mobile, pilih m-BCA kemudian pilih m-Transfer.'
            },
            {
                'image': "img/thank-you/mobile/mobile-2.png",
                'description': '2. Kemudian pilih opsi BCA Virtual Account.'
            },
            {
                'image': "img/thank-you/mobile/mobile-3.png",
                'description': '3. Masukkan nomor rekening BCA Virtual Account.'
            },
            {
                'image': "img/thank-you/mobile/mobile-4.png",
                'description': '4. Periksa jumlah bayar, masukkan pin, lalu selesaikan pembayaran.'
            },

        ]
    },
    'Mandiri Virtual Account': {
        'name': 'Mandiri',
        'method': {
            'name': 'Bank Transfer Virtual Account',
            'value': 'virtual-account'
        },
        'imagePath': '/img/bank/mandiri.png',
        'message': '',
        'atm': [
            {
                'image': "img/thank-you/atm/atm-transfer.png",
                'description': '1. Pada ATM, Pilih opsi Transaksi Lainnya, lalu pilih opsi Transfer',

            },
            {
                'image': "img/thank-you/atm/atm-virtual-account.png",
                'description': '2. Kemudian pilih opsi lainnya lagi dan pilih Multipayment.',

            },
            {
                'image': "img/thank-you/atm/atm-input-number.png",
                'description': '3. Masukkan kode perusahaan (XXXXX) diikuti No. Virtual Account.',

            },
            {
                'image': "img/thank-you/atm/atm-check.png",
                'description': '4. Masukkan jumlah bayar sampai 3 digit, lalu selesaikan pembayaran.'
            }
        ],
        'internet': [
            {
                'image': "img/thank-you/internet-banking/internet-transfer.png",
                'description': '1. Pada ATM, Pilih opsi Transaksi Lainnya, lalu pilih opsi Transfer',

            },
            {
                'image': "img/thank-you/internet-banking/internet-virtual-account.png",
                'description': '2. Kemudian pilih opsi lainnya lagi dan pilih Multipayment.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-number.png",
                'description': '3. Masukkan kode perusahaan (XXXXX) diikuti No. Virtual Account.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-check.png",
                'description': '4. Masukkan jumlah bayar sampai 3 digit, lalu selesaikan pembayaran.'
            },

        ]
    },
    'BNI Virtual Account': {
        'name': 'BNI',
        'method': {
            'name': 'Bank Transfer Virtual Account',
            'value': 'virtual-account'
        },
        'imagePath': '/img/bank/bni.png',
        'message': '',
        'atm': [
            {
                'image': "img/thank-you/atm/atm-transfer.png",
                'description': '1. Pada ATM, pilih opsi Transaksi lainnya, kemudian pilih opsi Transfer.'
            },
            {
                'image': "img/thank-you/atm/atm-virtual-account.png",
                'description': '2. Kemudian pilih pilih rekening tabungan kemudian pilih Rekening BNI.'
            },
            {
                'image': "img/thank-you/atm/atm-input-number.png",
                'description': '3. Masukkan nomor Virtual Account dan nominal transfer.',

            },
            {
                'image': "img/thank-you/atm/atm-check.png",
                'description': '4. Konfirmasi dan selesaikan pembayaran.'
            }
        ],
        'internet': [
            {
                'image': "img/thank-you/internet-banking/internet-transfer.png",
                'description': '1. Login ke iBanking BNI, pilih Transfer lalu atur dan tambah rekening tujuan.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-virtual-account.png",
                'description': '2. Masukkan nama, nomor VA dan kode otentifikasi token.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-number.png",
                'description': '3. Pilih transfer antar rekening BNI, '
                               'pilih Rekening Tujuan dan pilih Rekening Debit.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-check.png",
                'description': '4. Masukkan nominal bayar, kode otentifikasi token dan selesaikan pembayaran.'
            }
        ],
        'mobile': [
            {
                'image': "img/thank-you/mobile/mobile-1.png",
                'description': '1. Login ke mobile banking BNI, kemudian pilih transfer.',

            },
            {
                'image': "img/thank-you/mobile/mobile-2.png",
                'description': '2. Pilih menu antar rekening BNI, kemudian menu input rekening baru.',

            },
            {
                'image': "img/thank-you/mobile/mobile-3.png",
                'description': '3. Masukkan nomor rekening debit dan rekening tujuan.',

            },
            {
                'image': "img/thank-you/mobile/mobile-4.png",
                'description': '4. Masukkan password dan selesaikan pembayaran.'
            },

        ]
    },
    'Permata Virtual Account': {
        'name': 'Permata',
        'method': {
            'name': 'Bank Transfer Virtual Account',
            'value': 'virtual-account'
        },
        'imagePath': '/img/bank/permata.png',
        'message': '',
        'atm': [
            {
                'image': "img/thank-you/atm/atm-transfer.png",
                'description': '1. Pilih transfer, lalu transfer antar Rekening Permata Bank.'
            },
            {
                'image': "img/thank-you/atm/atm-virtual-account.png",
                'description': '2. Masukkan nomor virtual account.'
            },
            {
                'image': "img/thank-you/atm/atm-input-number.png",
                'description': '3. Pilih rekening yang akan di debit.',

            },
            {
                'image': "img/thank-you/atm/atm-check.png",
                'description': '4. Konfirmasi dan selesaikan pembayaran.'
            },

        ],
        'internet': [
            {
                'image': "img/thank-you/internet-banking/internet-transfer.png",
                'description': '1. Login ke iBanking Permata, pilih transfer.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-virtual-account.png",
                'description': '2. Pilih antar rekening PermataBank.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-number.png",
                'description': '3. Masukkan nomor rekening asal dan Virtual Account.',

            },
            {
                'image': "img/thank-you/internet-banking/internet-check.png",
                'description': '4. Masukkan kode SMS/Token dan transaksi selesai.'
            },

        ],
        'mobile': [
            {
                'image': "img/thank-you/mobile/mobile-1.png",
                'description': '1. Buka aplikasi Permata, pilih transfer.',

            },
            {
                'image': "img/thank-you/mobile/mobile-2.png",
                'description': '2. Pilih menu Antara Rekening Permata Bank.',

            },
            {
                'image': "img/thank-you/mobile/mobile-3.png",
                'description': '3. Masukkan nomor Rekening Asal & Virtual Account.',

            },
            {
                'image': "img/thank-you/mobile/mobile-4.png",
                'description': '4. Masukkan Kode SMS/Token & transaksi selesai.'
            },

        ],
        'other': [
            {
                'image': "img/thank-you/atm/atm-transfer.png",
                'description': '1. Buka aplikasi Permata, pilih transfer.',

            },
            {
                'image': "img/thank-you/atm/atm-virtual-account.png",
                'description': '2. (ATM Bersama Alto) Masukkan kode 013 + nomor virtual account.',

            },
            {
                'image': "img/thank-you/atm/atm-input-number.png",
                'description': '3. (Prima) Masukkan kode 013, lalu masukkan nomor Virtual Account.',

            },
            {
                'image': "img/thank-you/atm/atm-check.png",
                'description': '4. Konfirmasi dan selesaikan pembayaran.'
            },

        ]
    }
}

# META
META_SITE_PROTOCOL = 'https'
META_SITE_DOMAIN = 'jimshoneyofficial.com'
META_SITE_NAME = OSCAR_SHOP_NAME
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True

# GDN VARIABLE
DEFAULT_DAYS_AUTO_CANCELED = env.int('DAYS_CANCELED', 1)
DEFAULT_DAYS_AUTO_COMPLETE = env.int('DAYS_COMPLETE', 14)
GDN_FEE = env.string('GDN_FEE', '10')
ORDER_NUMBER_PREFIX = env.string('ORDER_NUMBER_PREFIX', 'JMS')

SITE_DESCRIPTION = "Jims Honey Official adalah Distributor Resmi produk Jims Honey di Indonesia. " \
                   "Jims Honey adalah Brand ternama dari Shanghai dengan produk yang sudah import " \
                   "hingga go International, termasuk Indonesia."
