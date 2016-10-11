# -*- coding: utf-8 -*-
#
# @author: Daemon Wang
# Created on 2016-05-04
#
# import ldap

LDAP_HOST = 'ldap://192.168.151.54'
LDAP_BASE_DN = 'dc=dhuicredit,dc=com'
MGR_CRED = 'cn=admin,dc=dhuicredit,dc=com'
MGR_PASSWD = 'dhui123'
STOOGE_FILTER = '(objectClass=*)'

class StoogeLDAPMgmt:

    def __init__(self, ldap_host=None, ldap_base_dn=None, mgr_cred=None,mgr_passwd=None):
        if not ldap_host:
            ldap_host = LDAP_HOST
        if not ldap_base_dn:
            ldap_base_dn = LDAP_BASE_DN
        if not mgr_cred:
            mgr_cred = MGR_CRED
        if not mgr_passwd:
            mgr_passwd = MGR_PASSWD
        # self.ldapconn = ldap.open(ldap_host)
        self.ldapconn = ldap.initialize(ldap_host)
        self.ldapconn.simple_bind(mgr_cred, mgr_passwd)
        self.ldap_base_dn = ldap_base_dn

    def list_stooges(self, stooge_filter=None, attrib=None):
        if not stooge_filter:
            stooge_filter = STOOGE_FILTER
        res = self.ldapconn.search_s('cn=test1,ou=test,dc=dhuicredit,dc=com', ldap.SCOPE_SUBTREE,STOOGE_FILTER, attrib)
        return res
        # if not stooge_filter:
        #     stooge_filter = STOOGE_FILTER
        # s = self.ldapconn.search_s(self.ldap_base_dn, ldap.SCOPE_SUBTREE,stooge_filter, attrib)
        # print "Here is the complete list of stooges:"
        # stooge_list = []
        # for stooge in s:
        #     attrib_dict = stooge[1]
        # for a in attrib:
        #     out = "%s: %s" % (a, attrib_dict[a])
        #     print out
        #     stooge_list.append(out)
        # return stooge_list

    def add_stooge(self, stooge_name, stooge_ou, stooge_info):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        stooge_attrib = [(k, v) for (k, v) in stooge_info.items()]
        print "Adding stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.add_s(stooge_dn, stooge_attrib)

    def modify_stooge(self, stooge_name, stooge_ou, stooge_attrib):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        print "Modifying stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.modify_s(stooge_dn, stooge_attrib)

    def delete_stooge(self, stooge_name, stooge_ou):
        stooge_dn = 'cn=%s,ou=%s,%s' % (stooge_name, stooge_ou, self.ldap_base_dn)
        print "Deleting stooge %s with ou=%s" % (stooge_name, stooge_ou)
        self.ldapconn.delete_s(stooge_dn)