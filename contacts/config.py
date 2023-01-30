class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432'

    CACHE_TYPE="redis"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_DB=0
    CACHE_REDIS_URL="redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT=500

