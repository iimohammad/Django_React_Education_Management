from rest_framework.versioning import AcceptHeaderVersioning

class DefaultVersioning(AcceptHeaderVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'
    
