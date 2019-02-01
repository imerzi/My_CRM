def get_module_from_endpoint(modules, endpoint):
    for m in modules:
        if 'endpoints' in m and endpoint in m['endpoints']:
            return m['label']
        elif 'endpoint' in m and endpoint == m['endpoint']:
            return m['label']
    return 'Null'
