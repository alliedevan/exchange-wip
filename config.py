import os

# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'ThisKeyBelongsInAnotherFile'

class DevelopmentConfig(BaseConfig):
	DEBUG = True

class ProductionConfig(BaseConfig):
	DEBUG = False
