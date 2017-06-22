class Config(object):
    DEBUG = False
    TESTING = False
    MYSQL_DATABASE_HOST='ascott.coxb3venarbl.ap-southeast-1.rds.amazonaws.com'


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = False
    TESTING = True
