from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'thess',                      # Or path to database file if using sqlite3.
        'USER': 'admin',                      # Not used with sqlite3.
        'PASSWORD': 'un beau pwd',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Solrsimplest version
# HAYSTACK_CONNECTIONS = {
# 'default': {
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://127.0.0.1:8983/solr',
#         'INCLUDE_SPELLING': True,
#         # ...or for multicore...
#         # 'URL': 'http://127.0.0.1:8983/solr/mysite',
#     },
# }

# Elastic search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack_fr.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '',  # set your ES address
        'INDEX_NAME': settings.PROJECT_NAME,
        # 'INCLUDE_SPELLING': True,   # not yet handled by ES
    },
}

# For redis
REDIS_PORT = 6379  # Please ask for a redis port to your administrator. Default value 6379, may already been used'

# # For django-rq, this mandatory to run rqworker command from manage.py
RQ_QUEUES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': REDIS_PORT,
        'DB': 0,
    },
}
