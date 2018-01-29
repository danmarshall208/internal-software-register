from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'

    # initialisation code
    def ready(self):
        # initialise ldap connection
        from .ldap import Ldap
        self.ldap = Ldap()
        self.ldap.connect()
