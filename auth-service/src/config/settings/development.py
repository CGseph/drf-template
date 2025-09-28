from .base import *  # noqa: F403

env = os.environ

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

redis_base_url = f"redis://{env.get('REDIS_HOST')}:{env.get('REDIS_PORT')}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{redis_base_url}/{env.get("REDIS_CACHE_DB")}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": env.get("REDIS_PASSWORD"),
            "SOCKET_CONNECT_TIMEOUT": int(env.get("REDIS_SOCKET_CONNECT_TIMEOUT")),
            "SOCKET_TIMEOUT": int(env.get("REDIS_SOCKET_TIMEOUT")),
            "IGNORE_EXCEPTIONS": bool(env.get("REDIS_IGNORE_EXCEPTIONS")),
        },
        "KEY_PREFIX": env.get("REDIS_CACHE_KEY_PREFIX"),
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{redis_base_url}/{env.get("REDIS_SESSION_DB")}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": env.get("REDIS_PASSWORD"),
            "SOCKET_CONNECT_TIMEOUT": int(env.get("REDIS_SOCKET_CONNECT_TIMEOUT")),
            "SOCKET_TIMEOUT": int(env.get("REDIS_SOCKET_TIMEOUT")),
            "IGNORE_EXCEPTIONS": bool(env.get("REDIS_IGNORE_EXCEPTIONS")),
        },
        "KEY_PREFIX": env.get("REDIS_SESSION_KEY_PREFIX"),
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"


REST_FRAMEWORK.setdefault(
    "DEFAULT_AUTHENTICATION_CLASSES",
    [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
)

REST_FRAMEWORK.setdefault(
    "DEFAULT_RENDERER_CLASSES",
    [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
)

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_OBJECT_CACHE_KEY_FUNC": "config.utils.generate_cache_key",
    "DEFAULT_LIST_CACHE_KEY_FUNC": "config.utils.generate_cache_key",
}
