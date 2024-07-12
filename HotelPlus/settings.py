from pathlib import Path
import dj_database_url
import django_heroku



# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = '6LeVDgUqAAAAAHsWMEtPDhKNd4e5iu_r-HP4Q7-K'
RECAPTCHA_PRIVATE_KEY = '6LeVDgUqAAAAANKwWVZaRJWXIvVtkQ_2Y40tk_A8'



BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d-n@01*)o_d6lxnijb^dikb5$9!1z+ab101=t9^x^%-n$gl+k%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# url de heroku genere: magestionhotel-c5b9754e0827.herokuapp.com/
ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'configuration',
    'users',
    'resto',
    'statistique',
    'chambre',
    'reservation',
    'paiement',

     # autres applications Django
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #auth google
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'HotelPlus.urls'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'configuration.context_processors.configuration_hotel',
            ],
        },
    },
]

WSGI_APPLICATION = 'HotelPlus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dfgdln8mtio5cs',
        'USER': 'u96s2lg8lborgb',
        'PASSWORD': 'pf8d4e9c394b0e968c8f449e8df57b6a79da53386cdcefc9708f36d1adf6009d3',
        'HOST': 'c7gljno857ucsl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "users.Users"


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Gestion des messagerie pour la reinitialisation de mot de passe
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Par exemple, smtp.gmail.com pour Gmail
EMAIL_PORT = 587  # Port SMTP de votre fournisseur de messagerie
EMAIL_USE_TLS = True  # Ou False si votre fournisseur de messagerie ne prend pas en charge TLS
EMAIL_HOST_USER = 'memouekone@esp.sn'  # Votre adresse e-mail
EMAIL_HOST_PASSWORD = 'chst eqjv vjgc dxst'  # Votre mot de passe e-mail

SITE_URL = 'http://localhost:8000'  # Changez cette valeur en fonction de votre URL de site


# la configuration pour le local

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


#authentification google 
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = 'home-users'
LOGOUT_REDIRECT_URL = '/'
# à revoir
SITE_ID = 4

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        
        'OAUTH_PKCE_ENABLED': True,

       # 'APP': {
        #    'client_id': '488004336723-u2ia0ckqq4p7c64o68pkqe167muh6m16.apps.googleusercontent.com',
        #    'secret': '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',
        #    'key': ''
        #}
        
    }


}


