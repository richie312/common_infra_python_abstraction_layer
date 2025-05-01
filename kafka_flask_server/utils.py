import json
import requests
from functools import wraps

cache_map = {}
ip = "localhost"
port = 5001
base_url = "http://{}:{}/".format(ip,port)


def incache_response(route, request):
    """
    Decorator to handle caching for Flask routes.
    :param route: The route to call if the data is not in the cache.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the request data is in the cache
            incoming_data = json.loads(request.data.decode('utf-8'))
            if str(incoming_data) in list(cache_map.keys()):
                value = cache_map[str(incoming_data)]
                cache_hit = True
            else:
                url = base_url + '/' + route
                value = requests.get(url)
                cache_map[str(incoming_data)] = value
                api_hit = True
            
            # Call the original function with the cached value
            return func(value, *args, **kwargs)
        
        return wrapper