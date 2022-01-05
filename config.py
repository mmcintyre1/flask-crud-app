import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    # if running on heroku, we use the database_url from the environment
    # need to hack the heroku database_url to work with sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', "").replace("://", "ql://", 1)


class DevelopmentConfig(Config):
    DEBUG = True

    # running locally via docker requires a POSTGRES_PASSWORD env variable
    # these need to have default values for when class is called
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    database = os.getenv('POSTGRES_NAME', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'postgres')
    port = os.getenv('POSTGRES_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{database}'
