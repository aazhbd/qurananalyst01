from qurananalyst.settings import * #@PydevCodeAnalysisIgnore

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'articulatelogic_com_qurananalyst',                      # Or path to database file if using sqlite3.
        'USER': 'qurananalyst@art',                      # Not used with sqlite3.
        'PASSWORD': 'IxcmmKQzQbTtqqN',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'qurananalyst@gmail.com'
EMAIL_HOST_PASSWORD = 'al_pass_2009'