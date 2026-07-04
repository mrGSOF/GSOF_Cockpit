try:
    # Python 3.9+
    from importlib import resources
    
    def getResourcePath(package, resource_subpath):
        with resources.as_file(resources.files(package).joinpath(resource_subpath)) as path:
            return str(path)

except (ImportError, AttributeError):
    # Older python versions
    import pkg_resources
    
    def getResourcePath(package, resource_subpath):
        return pkg_resources.resource_filename(package, resource_subpath)