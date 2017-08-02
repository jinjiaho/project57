# 1. Property-specific details
# Timezone string follows TZ format (see https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
PROP_NAME = "Ascott Raffles Place Singapore"
TIMEZONE = "Asia/Singapore"


# 2. Languages expected to be in use at this property
BABEL_LOCALES = ('en', 'zh', 'ms', 'ta')
BABEL_DEFAULT_LOCALE = "en"


# 3. MySQL DB connection details
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 'classroom'
MYSQL_DATABASE_DB = 'Ascott_InvMgmt'
MYSQL_DATABASE_HOST = 'ascott.coxb3venarbl.ap-southeast-1.rds.amazonaws.com'


# ADVANCED SETTINGS
SECRET_KEY = 'development-key'
UPLOADS_DEFAULT_DEST = 'static/img/items/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/img/items/'
UPLOADED_IMAGES_DEST = 'static/img/items/'
UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/items/'