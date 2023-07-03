def custom_preprocessing_hook(endpoints):
    """
    Filter documentation methods to only show retrieve and list.
    With the exception of users endpoints, and OpenAPI schema endpoints
    """
    filter = []
    for path, path_regex, method, callback in endpoints:
        if method == "GET":
            if "/api/schema/" not in path:
                filter.append((path, path_regex, method, callback))
        elif method == "POST":
            if "/api/token" not in path:
                filter.append((path, path_regex, method, callback))
        elif method == "PUT":
            if "/api/me/" not in path:
                filter.append((path, path_regex, method, callback))
        elif method == "PATCH":
            if "/api/me/" not in path:
                filter.append((path, path_regex, method, callback))
        else:
            filter.append((path, path_regex, method, callback))

    return filter
