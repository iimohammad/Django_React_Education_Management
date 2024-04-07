from rest_framework.versioning import AcceptHeaderVersioning

class DefualtVersioning(AcceptHeaderVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'
    
