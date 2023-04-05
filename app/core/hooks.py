def custom_preprocessing_hook(endpoints):
    filter = []
    """
    Filter documentation methods to only show retrieve and list.
    With the exception of users endpoints, and OpenAPI schema endpoints
    """
    for (path, path_regex, method, callback) in endpoints:
        if method == 'GET':
            if ('/api/schema/' not in path
                    and '/api/me/' not in path
                    and '/users/' not in path):
                filter.append((path, path_regex, method, callback))
    return filter
