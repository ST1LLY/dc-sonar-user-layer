"""
The file contains blank variables for further use in settings.py
Copy the file to sensitive_settings.py and fill in params
"""
S_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'web_app_db',
        'USER': 'dc_sonar_user_layer',
        'PASSWORD': '******',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

S_SECRET_KEY = '******'
S_SIGNING_KEY = '******'
S_AES_256_KEY = '******'
