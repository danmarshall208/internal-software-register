from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPSessionTerminatedByServerError
from .models import User
from django.conf import settings

# class to handle ldap connections
class Ldap():

    def connect(self):
        user = settings.LDAP_USER
        password = settings.LDAP_PASS
        server = Server('10.176.130.93', get_info=ALL)
        self.connection = Connection(server, user=user, password=password)
        self.connection.bind()


    def search(self, filter):
        try:
            self.connection.search(search_base='DC=apa,DC=gad,DC=schneider-electric,DC=com', search_filter=filter, search_scope=SUBTREE, attributes=['*'])
        except LDAPSessionTerminatedByServerError:
            self.connection.bind()
            self.connection.search(search_base='DC=apa,DC=gad,DC=schneider-electric,DC=com', search_filter=filter, search_scope=SUBTREE, attributes=['*'])
        return self.connection.entries


    # get a list of people that match a name (wildcard at end of string)
    def get_name(self, name):
        return self.search('(displayName=' + name + '*)')


    # get a single person from their sesa
    def get_sesa(self, sesa):
        results = self.search('(employeeID=' + sesa + ')')
        if len(results) == 0:
            return None
        else:
            return results[0]


    # sync a user with the directory
    def sync_user(self, user):
        self.sync_user_ldap(user)
        self.sync_manager_ldap(user)


    # sync all user details except their manager
    def sync_user_ldap(self, user):
        ldap_user = self.get_sesa(user.sesa)
        if ldap_user is None:
            user.active = False
        else:
            user.name = ldap_user.displayName.value
            user.email = ldap_user.mail.value
            user.DN = ldap_user.distinguishedName.value
            user.active = True
        user.save()


    # sync the manager details for a user
    def sync_manager_ldap(self, user):
        ldap_user = self.get_sesa(user.sesa)
        ldap_manager = self.get_sesa(ldap_user.sEguidManager.value)
        if ldap_manager is None:
            user.manager = None
        else:
            manager = User.objects.filter(sesa=ldap_manager.uid.value).first()
            if manager is None:
                manager = User(sesa=ldap_manager.uid.value)
            self.sync_user_ldap(manager)
            user.manager = manager
        user.save()


    def sync(self):
        for user in User.objects.all():
            self.sync_user(user)
