#!/usr/bin/env python
import re

out_dick = {
    "_ansible_no_log": False,
    "_ansible_verbose_always": True,

    "aelz_output":  {
        "changed": False,
        "failed": False,
        "output": "<?xml version=\"1.********\" encoding=\"UTF-8\"?><data xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.********\">\n        <ManagedElement xmlns=\"urn:com:ericsson:ecim:ComTop\">\n            <managedElementId>1</managedElementId>\n            <SystemFunctions>\n                <systemFunctionsId>1</systemFunctionsId>\n                <SecM xmlns=\"urn:com:ericsson:ecim:SecSecM\">\n                    <secMId>1</secMId>\n                    <UserManagement>\n                        <userManagementId>1</userManagementId>\n                        <LocalAuthenticationMethod xmlns=\"urn:com:ericsson:ecim:SecLA\">\n                            <localAuthenticationMethodId>1</localAuthenticationMethodId>\n                            <UserAccountM>\n                                <userAccountMId>1</userAccountMId>\n                                <UserAccount>\n                                    <userAccountId>TestEsmSuperUser</userAccountId>\n                                    <accountPolicy>ManagedElement=1,SystemFunctions=1,SecM=1,UserManagement=1,LocalAuthenticationMethod=1,AccountPolicy=1</accountPolicy>\n                                    <administrativeState>LOCKED</administrativeState>\n                                    <passwordPolicy>ManagedElement=1,SystemFunctions=1,SecM=1,UserManagement=1,LocalAuthenticationMethod=1,PasswordPolicy=1</passwordPolicy>\n                                    <userName>testEsm</userName>\n                                </UserAccount>\n                            </UserAccountM>\n                        </LocalAuthenticationMethod>\n                    </UserManagement>\n                </SecM>\n            </SystemFunctions>\n        </ManagedElement>\n    </data>\n"
                    },


    "changed": False,
    "failed": False
}

#print out_dick
print '*********************'
print ''
print ''

xml_str = out_dick["aelz_output"]["output"]
print xml_str
print '*********************'
print ''
print ''
#zz = xml_str.replace("xmlns=" ,  " |")
#print zz
t = re.sub('xmlns=.*?>', '', xml_str)
print t

print '*********************'
print ' original xml_str'
print ''
print xml_str

