def generate_cache_key(*args, **kwargs):
    request = kwargs.get("request")._request
    action = kwargs.get("view_instance").action

    return f"{action}:{request.method}{request.path}".replace("/", ":")
