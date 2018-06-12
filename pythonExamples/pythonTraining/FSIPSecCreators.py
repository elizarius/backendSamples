#!/usr/bin/python

# Standard Python classes
from sets import Set
import os
import re
import time
import socket
import platform
# Low level creator classes
import Common
import IPSecCommon
import NetworkObject
import IPSecObject
import Exceptions
import IPSecExceptions

# High level creator classes
import Deployment
import Convert
import IPSecConvert
import IPy
import IPUtils
import commands
from IPSecObject import DuplicatePolicy

##
# IPSec RecoveryGroup names in LDAP.
# Separate RGs for Redundant and NonRedundant IPSec deployment.
IPSecRedundantGroup      = 'IPSecRedundant'
IPSecNotRedundantGroup   = 'IPSec'
IPSecDefaultCertPath     = '/etc/ipsec/certs/'
IPSecDefaulCACertificate = 'cacert.pem'

IPSecDebug=False

fsgetcred_cmd="fsgetcred"
fssetcred_cmd="fssetcred "

##
# Helper function to verify is the script is running in development envrionment (LinSee)
# or in target environment.
def isLinSee():
    status, cred = commands.getstatusoutput('fsgetcred ldap fsLDAPRoot')
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0:
        return False
    else:
        return True


##
# Helper function to enter psk secrets to credentials service.
#
def setCredential(service, user, pwd):
    start=time.time()
    # Just open 1 the stream to process to enter the pwd
    status, cred = commands.getstatusoutput('fsgetcred ldap fsLDAPRoot')
    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0:
        # Credentials service found, this FP cluster. Proceed with set.
        Common.log().debug("Trying fssetcred to save IPSec PSK")
        cmdLine='fssetcred '+service+' '+user+' -c -p '
        try:
            put, get = os.popen4(cmdLine)
            put.write(pwd)
            put.close()
            Common.log().debug("Command executed in "+str(time.time()-start)+" seconds.")
        except ldap.LDAPError, le:
            raise Exceptions.LDAPError(le)

        # Must verify that pwd is stored and distributed before continuing. Seems that it
        # takes quite a long before credentials can be finally retrieved by clients.
        for wait in range(0,15):
            pwd = getCredentials(service, user)
            # Service returns this error message while it is distributed the password just entered. Just wait.
            if (pwd == "PASSWORD NOT ACCESSIBLE!"):
                if (wait == 15):
                    raise Exceptions.IPSecException("Failed to verify IPSec PSK from the Credentials service")
                time.sleep(1)
            else:
                time.sleep(1) # Extra sleep still needed for some reason???
                return True

    elif os.WIFEXITED(status) and os.WEXITSTATUS(status) == 127:
        # fssetcred command not found -> not in FS cluster
        Common.log().debug("Linsee environment, saving PSK to LDAP")
    else:
        raise IPSecException("fsgetcred WEXITED STATUS %d" % (os.WEXITSTATUS(status)))

    return False

##
# Helper function to remove the psk entry from the credentials service.
#
def delCredentials(service, user):
    start=time.time()
    # Just open the stream to process to enter the pwd"
    cmdLine='fssetcred '+'IPSec'+service+' '+user+" -d"
    put, get = os.popen4(cmdLine)
    put.close()
    Common.log().debug("Command ("+cmdLine+") for deleting IPSec PSK executed in "+str(time.time()-start)+" seconds.")

    
##
# Helper function to read psk secrets from credential services.
#
def getCredentials(service, user):
    start=time.time()
    # Just open the stream to process to enter the pwd"
    cmdLine='fsgetcred '+service+' '+user
    status, pwd = commands.getstatusoutput(cmdLine)
    if (pwd == "PASSWORD NOT ACCESSIBLE!"):
        pwd = None
    else:
        Common.log().debug("Command ("+cmdLine+") executed in "+str(time.time()-start)+" seconds. Result: "+pwd)
    return pwd


##
# Helper function to return virtualHost name if IPSec config of the node is located
# under VirtualHost fragment.
#
def virtualHostFromNode(node):   
    if len(node) < 2:
        raise Exceptions.UnderspecifiedError("Invalid node name %s" % (node))
    virtualHost='IPSec'+node[0:len(node)-2]
    
    return virtualHost


##
# Helper function to determine if the given node belongs to ActiveStandby group from IPSec point of view.
#
def isActiveStandbyIPSec(node):
    """ Has this node IPSec RecoveryGroup deployed with ActiveStandby RecoverPolicy setting?
        If yes, IPSec config of this node is shared between Active-Standby node pair and placed
        under VirtualHosts fragment.
        If no, IPSec config is node specific and placed under nodes fragment.
    """
    if not len(node):
        IPSecException.IPSecError("Missing node name")
    
    # First check if the node has IPSecRedundant recovery group
    IPSecActiveStandbyList = Deployment.getRecoveryGroups({"fshaRecoveryGroupName": IPSecRedundantGroup, "fshaRecoveryPolicy": 'ColdActiveStandby'})
    IPSecnodelist = []
    for rg in IPSecActiveStandbyList:
        IPSecnodelist.extend(IPSecActiveStandbyList[rg]['node'])
    if node in IPSecnodelist:
        return True

    # Then the node should has NoRedundancy IPSec Recovery Group
    IPSecNotRedundantList = Deployment.getRecoveryGroups({"fshaRecoveryGroupName": IPSecNotRedundantGroup, "fshaRecoveryPolicy": 'NoRedundancy'})
    IPSecnodelist = []
    for rg in IPSecNotRedundantList:
        IPSecnodelist.extend(IPSecNotRedundantList[rg]['node'])
    if node in IPSecnodelist:
        return False
    else:
        return False
        # Not either of IPSec Recovery groups found, invalid deployment?
        raise Exceptions.ObjectNotExistError(msg="No IPSec RecoveryGroup found from LDAP for node %s" % (node))

     
##
# Helper function to check if Global settings has been defined yet.
#
def isGlobalSet(node=None, vrf=0):
    """ Check if global settings has been defined, which is required for other
        objects.
    """
    if (node==None):
        return False

    key = IPSecObject.FSIPSecGlobal()
    key.setAttribute("fsIPSecVRFId", vrf)
    
    ret_list = []
    try:
        ret_list = getIPSecObjectList(key, name="0", node=node)
    except:
        pass

    # No global objects found for this node
    if ret_list != None:
        return True
    
    return False

##
# Helper function to check if Global settings has been defined yet. Additionl
# 'ike' parameter may be use to check what is global setting for IKE version-
#
def isGlobalIke(ike, node=None, vrf=0):
    """ Check if the IKE version given matches with the global IKE version settings.
    """
    ret_list = []

    if not isGlobalSet(node, vrf):
        raise IPSecExceptions.ConfigError("No global settings found from node %s" % (node))

    key = IPSecObject.FSIPSecGlobal()
    key.setAttribute("fsIPSecVRFId", vrf)

    ret_list = []
    try:
        ret_list = getIPSecObjectList(key, name="0", node=node)
    except:
        pass

    if (ike == ret_list.getAttribute("fsIPSecVPNIkeVersion").get()[0]):
        return True
    else:
        return False


    
##
# Helper function to find given IPSec objects or the one selected by the name
#
def getIPSecObjectList(object, name=None, node=None):
    """ find all objects of the given type or just single instance if the name parameter was given.
    """ 
    ret_list = []
    if node == None:
        base="fsClusterId=ClusterRoot"
    else:    
        if isActiveStandbyIPSec(node):
            host=virtualHostFromNode(node)
            base=IPSecObject.getVirtualHostBaseDN(host)
        else:
            base=IPSecObject.getHostBaseDN(node)
            host=node


    if object.getObjectClass() in IPSecObject.objectClasses:        
        key = object
        if (object.getObjectClass() == 'FSIPSecGlobal'):
            if name != None: # Not really an option, name (VRF) 0 only is supported now.
                key.setAttribute("fsIPSecVRFId", name)
            else:
                key.setAttribute("fsIPSecVRFId", '0')
        if (object.getObjectClass() == 'FSIPSecVPNTemplate') and name != None:
            key.setAttribute("fsIPSecVPNTemplateName", name)
        if (object.getObjectClass() == 'FSIPSecVPN') and name != None:
            key.setAttribute("fsIPSecVPNName", name)
        if (object.getObjectClass() == 'FSIPSecRule') and name != None:
            key.setAttribute("fsIPSecRuleName", name)
                        
        try:
            ret_list = key.get(base=base, host=host)
        except:
            pass
    else:
        raise Exceptions.UnderspecifiedError("Unknown object!")
    
    # If we are expecting one item, return only one instance, if found
    if name != None:
        if len(ret_list) == 1:
            return ret_list[0]
        else:
            return None
    # ... else return the whole list
    else:
        return ret_list

##
# Helper function to find IPSec object referred by another
#
def getIPSecObjectsWithReference(object, name, node=None):
    """ find all objects of the given type matching the given filter string.
    """
    ret_list = []
    key = object
    
    if node == None:
        base="fsClusterId=ClusterRoot"
    else:
        if node._isVirtualHost:
            host=virtualHostFromNode(node._node)
            base=IPSecObject.getVirtualHostBaseDN(node._virtualHost)
        else:
            base=IPSecObject.getHostBaseDN(node._node)
            host=node._node
        
    if object.getObjectClass() in IPSecObject.objectClasses:      
        if (object.getObjectClass() == 'FSIPSecVPNTemplate'):
            key.setAttribute("fsIPSecVPNTemplateName", name)
        else:
            if (object.getObjectClass() == 'FSIPSecVPN'):
                key.setAttribute("fsIPSecVPNTemplateName", name)
            else:
                if (object.getObjectClass() == 'FSIPSecRule'):
                    key.setAttribute("fsIPSecRuleVPNName", name)
                else:
                    return ret_list

        try:
            ret_list = key.get(base=base, host=host)
        except:
            pass

    return ret_list

##
# Helper function to find given IPSec objects or the one selected by the name
#
def getIPSecRuleList(object, name=None):
    """ find all objects of the given type or just single instance if the name parameter was given.
    """ 
    ret_list = []
    
    base =  "fsFragmentId=VirtualHosts,%s" % (object.base,)
    naming_attribute = 'fsIPSecRuleVPNName'
    ret_list = IPSecObject.getObjects(None, {'objectClass': [object.getObjectClass()], naming_attribute : [name]}, base)
    return ret_list
        


##
# Helper function to find IP address instances based on address and family
#
def findAddresses(node, addr, family, length=None, type=None):
    """ Find all address instances that have mathing IP address and family
    """
    retList = []
    filter = dict(fsipIPAddressFamily=[family],\
                  fsipIPAddress=[addr])
    if type:
        filter['fsipIPAddressType']= [type]

    addrList = NetworkObject.getNetworkObjects("FSIPIPAddr", filter)

    if node._isVirtualHost:
        for a in addrList:
            # If RGs are linked, address may belong to other than IPSecRedundant group too????
            if a.isVirtual(): # and a.getHost() == "IPSecRedundant":
                vhlinkKey = NetworkObject.FSIPVirtualHostLink()
                vhlinkKey.setAttribute("fsipVirtualHostLinkTarget", [a.getHost()])
                vhlinkList = vhlinkKey.get()
                if (len(vhlinkList) > 0):
                    # Found a link to the virtualHost where the address is
                    retList.append(a)
                                                                       
    else:
        for a in addrList:
            if node._node == a.getHost():
                retList.append(a)
        # If not found from dedicated addresses, also check the virtual addresses
        if not len(retList):
            for a in addrList:
                if a.isVirtual():
                    vhlinkKey = NetworkObject.FSIPVirtualHostLink()
                    vhlinkKey.setAttribute("fsipVirtualHostLinkTarget", [a.getHost()])
                    vhlinkList = vhlinkKey.get()
                    if len(vhlinkList) > 0:
                        # Found a link to the virtualHost where the address is 
                        retList.append(a)
    return retList

##
# Helper function to check if the subnets are overlapping.
#
def isNetOverlapping(net_a, net_b):
    """ Check if the subnets are overlapping.
    """
    return False
    net_a = IPy.IP(net_a)
    net_b = IPy.IP(net_b)

    if net_a.ip >= net_b.ip and net_a.ip < net_b.ip + net_b.len():
        return True
    if net_b.ip >= net_a.ip and net_b.ip < net_a.ip + net_a.len():
        return True
    
    return False

##
# Helper function to check if address belongs to a subnet
#
def netContains(net, address):
    """Check if net contains IP.
    Returns 0 if the two ranges don't overlap, 1 if the given
    range overlaps at the end and -1 if it does at the beginning.
    """  
    network = IPy.IP(net)
    ip      = IPy.IP(address)
    if ip.ip >= network.ip and ip.ip < network.ip + network.len():
        return True
    return False

    
class IPSecNode:
    """ Base node class for node related data.

    """
    def __init__(self, object, mo):
        self._node = mo.getNode()
        self._redundantNode0 = None
        self._redundantNode1 = None
        self._base           = None
        self._virtualHost     = None
#        if mo.type() == 'virtualhost':
#            # We shouldn't come here ...
#            print "VirtualHost"
            
        if isActiveStandbyIPSec(self._node):
            self._isVirtualHost = True
            self._redundantNode0 = self._node[0:len(self._node)-2]+'-0'
            self._redundantNode1 = self._node[0:len(self._node)-2]+'-1'
            self._virtualHost='IPSec'+self._node[0:len(self._node)-self._node.index('-')+1]
            self._base = object.getBase(host=self._virtualHost, virtualhost=True)
        else:
            self._isVirtualHost = False
            self._base = object.getBase(host=self._node, virtualhost=False)
            

##
# IPSec Creator class. A parent class of other creator classes. Mainly for debuggin purposes.
#
class IPSecCreator:
    """ IPSec Creator class.
    """
    def __init__(self):
        if IPSecDebug:
            test = 1
    def add(self, object, name):
        """ Creator add method.
        """
        if IPSecDebug == True:
            print self.__doc__
            print object

    
##
# IPSec Global creator
#
class IPSecGlobal(IPSecCreator):
    
    # Constructs FSIPSecGlobal object.
    #
    # @param ike          Global IKE version if both versions are not supported simultaneously.
    # @param mo           The list of objects, translated from an owner of the VLAN iface. For more info see MONameConv
    # @param pskpath      PSK file path if different from the default.     
    # @param certpath     Path for certificates, if different from the default.
    # @param ike1include  Include file for IKEv1 external config file (racoon.conf).
    # @param ike1include  Include file for IKEv2 external config file (ipsec.conf)
    # @param cacertfile   CA certifacte file name, if different from the default. 
    # @param activation   Global IPSec activatation, currently always enabled.
    """ IPSec Global Creator. Manages FSIPSecGloba object.
    """   
    def __init__(self, ike=1, molist=[], pskpath=None, certpath=None, cacertfile=None, \
                 ike1include=None, ike2include=None, activation="enable", vrfId=0, configPath=None):
        self._nodelist    = []
        self._activation  = activation
        self._ike         = ike
        self._pskpath     = pskpath
        self._certpath    = certpath
        self._cacertfile  = cacertfile
        self._ike1include = ike1include
        self._ike2include = ike2include
        self._vrfId       = vrfId
        self._configPath  = configPath
        nodelist = []
        for mo in molist:
            self._nodelist.append(IPSecNode(IPSecObject.FSIPSecGlobal(), mo))
            
    def fill(self, common):
        common.setAttribute("fsIPSecGlobalActivation",           [self._activation])     
        common.setAttribute("fsIPSecVPNIkeVersion",              [self._ike])
        common.setAttribute("fsIPSecVRFId",                      [self._vrfId])
        if (self._pskpath != None):
            common.setAttribute("fsIPSecGlobalPSKFilePath",      [self._pskpath])
        if self._certpath != None:
            common.setAttribute("fsIPSecGlobalCertificatePath",  [self._certpath])
        if self._cacertfile != None:
            common.setAttribute("fsIPSecGlobalCACertificate",    [self._cacertfile])
        if self._ike1include != None:
            common.setAttribute("fsIPSecGlobalIKE1Include",      [self._ike1include])
        if self._ike2include != None:                
            common.setAttribute("fsIPSecGlobalIKE2Include",      [self._ike2include])
        if self._configPath != None:
            common.setAttribute("fsIPSecConfigPath",             [self._configPath])
            
        return common

    def validate(self):
        return
    
    def validateInstance(self, common):
        for n in self._nodelist:
            # Golbal object must be created first, but just for sure, check there
            # are no VPN objects already under this node, that might be fatal.
            vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), node=n._node)
            if len(vpn_list) > 0:
                # If there are already VPNs configured, the common settings cannot be modified - without deleting VPNs first.
                if isGlobalSet(n._node, self._vrfId):
                    raise IPSecExceptions.ConfigError("IPSec common object already configured in the node %s" % (n._node))
                else:
                    for v in vpn_list:
                        if (common.getAttribute("fsIPSecVPNIkeVersion").get()[0] !=  v.getAttribute("fsIPSecVPNIkeVersion").get()[0]):
                            raise IPSecExceptions.IPSecError("Conflicting IKE version in VPN %s " % (v.getAttribute("fsIPSecVPNName").get()[0]))
    
        
    ##
    # Adds the global object to the LDAP.
    #
    def add(self):
        """ Adds the global object to the LDAP.
        """
	print 'AELZ add()  step 1 pass'
        common = self.fill(IPSecObject.FSIPSecGlobal())            
        common.fillDefaults()
        self.validate()
        IPSecCreator.add(self, globals, 'global')
        self.validateInstance(common)

        if not isLinSee():
            # Add openssl link for racoon certificate verification against the issuer's certificate
            # in the certificate directory:
            # ln -s cacert.pem 'openssl x509 -noout -hash -in cacert.pem'.0
            #
            # If the certificate directory is changed, we must be running in the selected node for link creation            
            if self._certpath != None:
                for n in self._nodelist:
                    # Can't add the link unless we are in the node, right?
                    if platform.node() != n._node:
                        raise IPSecExceptions.ConfigError("Certificate path configuration must be exeucted in the owner node %s" % (n._node))
                certPath=self._certpath+'/'
            else:
                certPath=IPSecDefaultCertPath

	    print 'AELZ add()  pass 2  certPath : ' , certPath 
                
            # CA certificate name can be anything, we just have to change it to our link creation commands.
            if self._cacertfile != None:
                cacert=self._cacertfile
            else:
                cacert=IPSecDefaulCACertificate
                
	    print 'AELZ add()  pass 3  CA cert name  : ' , cacert 
            # In default directory case create the hash link is to be distributed to every node
            # Create the link to the state-volume for distribution
            if self._certpath == None:
                os.chdir("/mnt/mstate/_global/"+certPath)
            else:
                os.chdir(certPath)
            linkCmd="ln -s "+cacert+" 'openssl x509 -noout -hash -in "+cacert+"'.0"
                
            # Create link if it does not exist yet.
            if not os.path.exists("openssl x509 -noout -hash -in "+cacert+".0"):
                status, output = commands.getstatusoutput(linkCmd)
                if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
                    # If file exists already, we shouldn't get any complaints from openssl                    
                    if os.path.islink(certPath+'/'+cacert):
                        raise IPSecExceptions.ConfigError("Unable to generate openssl hash link to %s" % cacert)
                    
            # We also have to add a link for strongswan ca certificates - seems like they don't accept absolute path??
            # Create the link to the state-volume for distribution
            os.chdir("/mnt/mstate/_global/etc/ipsec/certs/ipsec.d/cacerts/")
           
            #AELZ fix .
            tempC='/mnt/mstate/_global/etc/ipsec/certs/ipsec.d/cacerts/'  
            if certPath == tempC:
               raise IPSecExceptions.ConfigError("Not allowed certificate path  %s" % certPath)

            linkCmd="ln -s "+certPath+cacert+" "+cacert
            status, output = commands.getstatusoutput(linkCmd)
            if os.WIFEXITED(status) and os.WEXITSTATUS(status) != 0:
                # Return 1 if the link exists already, don't care about that.
                if os.WEXITSTATUS(status) != 1:
                    raise IPSecExceptions.ConfigError("Failed to generate link from %s to %s" % (certPath+cacert, "/etc/ipsec/certs/ipsec.d/cacerts/"))
            
            
            
        for n in self._nodelist:
            common.setAttribute("fsIPSecObjectOwner", [n._node])
            common.add(n._node, n._base, force=DuplicatePolicy.ALLOW_DUPLICATE, virtualhost=n._isVirtualHost)
        # Run fsdistribute to distribute the links related to the CA certificate files. User must do the
        # same for the CA certificate files and keys himself. If any certificate files have been installed to
        # the distribution directory, they will be now distributed too.
        status, output = commands.getstatusoutput("fsdistribute /mnt/mstate/_global/etc/ipsec/certs/")

    ##
    # Modifies existing global instance in the LDAP.
    #
    def modify(self):
        # Get the current object
        global_list = getIPSecObjectList(IPSecObject.FSIPSecGlobal())
        if not len(global_list):
            raise IPSecExceptions.IPSecError("IPSec common object was not found in virtual node %s" % (node))
        for g in global_list:
            if self._pskpath != None:
                g.setAttribute("fsIPSecGlobalPSKFilePath",       [self._pskpath])
            if self._ike != None:
                vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), node=n._node)
                for vpn in vpn_list:
                    if (self._ike != vpn.getAttribute("fsIPSecVPNIkeVersion").get()[0]):
                        raise IPSecExceptions.ConfigError("Incompatible IKE version %d found in VPN %s " \
                                                         % (vpn.getAttribute("fsIPSecVPNName").get()[0], vpn.getAttribute("fsIPSecIkeVersion").get()[0]))
                    else:
                        g.setAttribute("fsIPSecVPNIkeVersion",           [self._ike])
            if self._certpath != None:
                g.setAttribute("fsIPSecGlobalCertificatePath",   [self._certpath])
            if self._cacertfile != None:
                g.setAttribute("fsIPSecGlobalCACertificate",     [self._cacertfile])                
            if self._ike1include != None:
                g.setAttribute("fsIPSecGlobalIKE1Include",       [self._ike1include])
            if self._ike2include != None:                
                g.setAttribute("fsIPSecGlobalIKE2Include",       [self._ike2include])

        for n in self._nodelist:
            global_list[0].modify(n._node, base=None)

    ##
    # Deletes the global object from the LDAP database.
    #
    def delete(self):
        for n in self._nodelist:
            key = IPSecObject.FSIPSecGlobal()
            key.setAttribute("fsIPSecVRFId", '0')
            global_list = key.get(base=n._base)

            global_list = getIPSecObjectList(IPSecObject.FSIPSecGlobal(), node=n._node)
            if not len(global_list):
                raise Exceptions.ObjectNotExistError(msg="Nothing to delete in node %s" % (n._node))            
            vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), node=n._node)
            if len(vpn_list) > 0:
                raise IPSecExceptions.ConfigError("Cannot delete global settings if any VPNs exists.")
            
            if not isLinSee():
                # Add openssl link for CA certificate verification
                if global_list[0].getAttribute("fsIPSecGlobalCertificatePath").get():
                    certPath=global_list[0].getAttribute("fsIPSecGlobalCertificatePath").get()[0]+'/'
                    if platform.node() != n._node:
                        raise IPSecExceptions.ConfigError("Common configuration delete must be exeucted in the owner node %s" % (n._node))
                    os.chdir(certPath)
                else:
                    certPath=IPSecDefaultCertPath
                    os.chdir("/mnt/mstate/_global/"+certPath)
                
                if global_list[0].getAttribute("fsIPSecGlobalCACertificate").get():
                    cacert=global_list[0].getAttribute("fsIPSecGlobalCACertificate").get()[0]
                    if platform.node() != n._node:
                        raise IPSecExceptions.ConfigError("Common configuration delete must be exeucted in the owner node %s" % (n._node))
                else:
                    cacert=IPSecDefaulCACertificate

	        print 'AELZ delete()  pass 5  CA cert name  : ' , cacert 
                # AELZ fix 1 .
                linkCmd="rm -f 'openssl x509 -noout -hash -in "+cacert+"'.0"
        
                # If the link (is link and) exists, remove it
                if os.path.islink("openssl x509 -noout -hash -in "+cacert+".0"):
                    status, cred = commands.getstatusoutput(linkCmd)
                    if os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0:
                        if os.path.islink("openssl x509 -noout -hash -in "+cacert+".0"):
                            errorLnk="'openssl x509 -noout -hash -in "+cacert+"'.0"
                            raise IPSecExceptions.ConfigError("Failed to remove openssl hash link for CA certificate %s" % (errorLnk))
                # Also remove the link in the Strongswan cacert directory
                if platform.node() != n._node:
                    raise IPSecExceptions.ConfigError("Common configuration delete must be exeucted in the owner node %s" % (n._node))
                
                # to the state-volume for distribution , AELZ fix2 , add -f into remove command .
                os.chdir("/mnt/mstate/_global/etc/ipsec/certs/ipsec.d/cacerts/")
                if  os.path.exists(cacert) and os.path.islink(cacert):
                    linkCmd="rm -f  "+cacert
                    status, output = commands.getstatusoutput(linkCmd)
                
            global_list[0].delete(n._node, base=n._base)
            if not isLinSee():
                status, output = commands.getstatusoutput("fsdistribute /mnt/mstate/_global/etc/ipsec/certs/")
            
        
##
# IKEv1 Template creator
#
class IKE1Template(IPSecCreator):
    #
    # Constructs IKE version 1 Template
    #
    # @param name        Name of the template.
    # @param ike         IKE version of this template - must be 1.     
    # @param dscpcopy    Enables DSCP header copy to IPSec packets. =============== OBSOLATE =================
    # @param exitpolicy  Forces the use of exit policy for icoming packets.
    # @param mode        IKE mode.
    # @param p1enc       Phase 1 encryption algorithm.
    # @param p1hash      Phase 1 hash  algorithm.
    # @param p1lifetime  Phase 1 lifetime.
    # @param p1dhgroup   Phase 1 Diffie-Hellman Group
    # @param p1auth      Phase 1 Authentication method
    # @param p1idtype    Phase 1 Id type to be used.
    # @param p2enc_list  Phase 2 encryption algorithms.
    # @param p2lifetime  Phase 2 lifetime.
    # @param p2pfsgroup  Phase 2 PFS Group
    # @param p2auth_list Phase 2 Authentication algorithms.
    """ IKEv1 Template Creator. Manages the FSIPSecVPNTemplate objects. 
    """   
    def __init__(self, name, ike='1', exitpolicy=None, mode="main", \
                 p1enc=None, p1hash=None, p1lifetime=None, p1dhgroup=None, p1auth=None, \
                 p1idtype=None, p2enc_list=[], p2lifetime=None, p2pfsgroup=None, p2auth_list=[], \
                 dpddelay=None, dpdretry=None, dpdmaxfail=None,molist=[]):
        self._nodelist    = []
        self._name        = name
        self._ike         = ike
#        self._dscpcopy    = dscpcopy
        self._exitpolicy  = exitpolicy
        self._mode        = mode
        self._p1enc       = p1enc
        self._p1hash      = p1hash
        self._p1lifetime  = p1lifetime
        self._p1dhgroup   = p1dhgroup
        self._p1auth      = p1auth
        self._p1idtype    = p1idtype
        self._p2enc_list  = p2enc_list
        self._p2lifetime  = p2lifetime
        self._p2pfsgroup  = p2pfsgroup
        self._p2auth_list = p2auth_list
        self._dpddelay    = dpddelay
        self._dpdretry    = dpdretry
        self._dpdmaxfail  = dpdmaxfail
          
        for mo in molist:
            self._nodelist.append(IPSecNode(IPSecObject.FSIPSecVPNTemplate(), mo))

        self.validate()
    #
    # Fills the mandatory command line attributes to the instance.
    #
    # @param template  Instance where to fill the attributes.
    # @returns         The filled template instance.
    def fill(self, template):
        template.setAttribute("fsIPSecVPNIkeVersion",        [self._ike])
        template.setAttribute("fsIPSecVPNTemplateName",      [self._name])
 #       template.setAttribute("fsIPSecDSCPCopy",             [self._dscpcopy])
        template.setAttribute("fsIPSecExitPolicy",           [self._exitpolicy])
        if self._mode != None:
            template.setAttribute("fsIPSecIKEMode",              [self._mode])
        template.setAttribute("fsIPSecPhase1Encryption",     [self._p1enc])
        template.setAttribute("fsIPSecPhase1Hash",           [self._p1hash])
        template.setAttribute("fsIPSecPhase1LifeTime",       [self._p1lifetime])
        template.setAttribute("fsIPSecPhase1DHGroup",        [self._p1dhgroup])
        template.setAttribute("fsIPSecPhase1Authentication", [self._p1auth])
        template.setAttribute("fsIPSecPhase1IdentifierType", [self._p1idtype])
        template.setAttribute("fsIPSecPhase2Encryption",     list(self._p2enc_list))
        template.setAttribute("fsIPSecPhase2LifeTime",       [self._p2lifetime])
        if self._p2pfsgroup != None:
            template.setAttribute("fsIPSecPhase2PFSGroup",       [self._p2pfsgroup])
        template.setAttribute("fsIPSecPhase2Authentication", list(self._p2auth_list))        
        if self._dpddelay != None:
            template.setAttribute("fsIPSecDPDDelay",         [self._dpddelay])
        if self._dpdretry != None:
            template.setAttribute("fsIPSecDPDRetry",         [self._dpdretry])
        if self._dpdmaxfail != None:
            template.setAttribute("fsIPSecDPDMaxFail",       [self._dpdmaxfail])       
        return template
    #
    # Validates the command line attributes.
    #
    def validate(self):
        """ Validates the command line attributes.
        """
        if (self._dpddelay == None) and (self._dpdretry != None or self._dpdmaxfail != None):           
            raise Exceptions.ParseError("Missing dpddelay value")

    #
    # Validates created template instance and associations.
    #
    # @param template  Complete template instance to be validated.
    #.
    def validateInstance(self, template):
        for n in self._nodelist:
            vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), template.getAttribute("fsIPSecVPNTemplateName").get()[0], node=n._node)

        # If aggressive mode is used, pfs group must be same for all proposals!

        
    ##
    # Adds the template object to the LDAP.
    #
    def add(self):
        self.validate()
        
        # First check if a Template with this name exists. We cannot overwrite is since
        # some VPNs may refer to it and they would be affected by the change of the Template.
#        for n in self._nodelist:
#            temp = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._name, n._node)
            # Allow duplicate templates now, still only one instance remains.
            # There shouldn't be any 'loose' VPNs referring to non-existent Template, but
            # to be sure, just check if anyone is referring to this name.
#            vpn_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecVPN(), self._name, node=n)
#            if len(vpn_list):
#                raise IPSecExceptions.ConfigError("Template name already referred by an existing VPN - delete it first")

        # Create template and fill mandatory
        template = self.fill(IPSecObject.FSIPSecVPNTemplate())
        template.fillDefaults()
        
        IPSecCreator.add(self, template, 'template')
        
        if (self._dpddelay != None):
            template.setAttribute("fsIPSecDPDDelay",             [self._dpddelay])
        if (self._dpdretry != None):
            if (self._dpddelay == None) or (self._dpddelay == 0):
                raise Exceptions.ParseError("DPD settings has no effect unless delay is non-zero ")   
            template.setAttribute("fsIPSecDPDRetry",             [self._dpdretry])
        if (self._dpdmaxfail != None):
            if (self._dpddelay == None) or (self._dpddelay == 0):
                raise Exceptions.ParseError("DPD settings has no effect unless delay is non-zero ")
            template.setAttribute("fsIPSecDPDMaxFail",           [self._dpdmaxfail])

        # Validate template instance.
        self.validateInstance(template)
        
        # Add object to the LDAP database.
        for n in self._nodelist:
            template.setAttribute("fsIPSecObjectOwner", [n._node])
            template.add(n._node, n._base, force=DuplicatePolicy.ALLOW_DUPLICATE, virtualhost=n._isVirtualHost)


    ##
    # Deletes the template object from the LDAP database.
    #
    def delete(self):
        # Find the template object to be deleted.
        for n in self._nodelist:
            del_temp = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._name, n._node)
            if del_temp == None:
                raise Exceptions.ObjectNotExistError(msg="Nothing to delete in node %s" % (n._node))
            vpn_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecVPN(), self._name, node=n)
            if len(vpn_list):
                raise IPSecExceptions.ConfigError("Cannot delete a template that is referred by VPN")
        for n in self._nodelist:
            del_temp.delete(n._node, n._base)

##        
# IKEv2 Template creator
#
class IKE2Template(IPSecCreator):
    #
    # Constructs IKE version 2 Template
    #
    # @param name        Name of the template.
    # @param ike         IKE version of this template - must be 1.     
    # @param dscpcopy    Enables DSCP header copy to IPSec packets.  ========== OBSOLATE ==========================
    # @param exitpolicy  Forces the use of exit policy for icoming packets.
    # @param p1enc       Phase 1 encryption algorithm.
    # @param p1hash      Phase 1 hash  algorithm.
    # @param p1lifetime  Phase 1 lifetime.
    # @param p1dhgroup   Phase 1 Diffie-Hellman Group
    # @param p1auth      Phase 1 Authentication method
    # @param p1idtype    Phase 1 Id type to be used.
    # @param p2enc_list  Phase 2 encryption algorithms.
    # @param p2lifetime  Phase 2 lifetime.
    # @param p2pfsgroup  Phase 2 PFS Group
    # @param p2auth_list Phase 2 Authentication algorithms.
    # @param mode        IKE mode - always main. Just keep it for future support of other modes.    
    # @param dpdaction   DPD action type.
    # @param dpdinterval DPD time interval.
    """ IKEv2 Template Creator. Manages the FSIPSecVPNTemplate objects. 
    """   
    def __init__(self, name, ike=2, exitpolicy=None, \
                 p1enc=None, p1hash=None, p1lifetime=None, p1dhgroup=None, p1auth=None, p1idtype=None, \
                 p2enc_list=[], p2lifetime=None, p2pfsgroup=None, p2auth_list=[], \
                 mode="main", dpdaction=None, dpdinterval=None, molist=[]):
        self._nodelist    = []
        self._name        = name
        self._ike         = ike
#        self._dscpcopy    = dscpcopy
        self._exitpolicy  = exitpolicy
        self._p1enc       = p1enc
        self._p1hash      = p1hash
        self._p1lifetime  = p1lifetime
        self._p1dhgroup   = p1dhgroup
        self._p1auth      = p1auth
        self._p1idtype    = p1idtype
        self._p2enc_list  = p2enc_list
        self._p2lifetime  = p2lifetime
        self._p2pfsgroup  = p2pfsgroup
        self._p2auth_list = p2auth_list
        self._mode        = mode        
        self._dpdaction   = dpdaction
        self._dpdinterval = dpdinterval        

        for mo in molist:
            self._nodelist.append(IPSecNode(IPSecObject.FSIPSecVPNTemplate(), mo))
            
    #
    # Fills the mandatory command line attributes to the instance.
    #
    # @param template  Instance where to fill the attributes.
    # @returns         The filled template instance.
    def fill(self, template):
        template.setAttribute("fsIPSecVPNTemplateName",      [self._name])
        template.setAttribute("fsIPSecVPNIkeVersion",        [self._ike])
 #       template.setAttribute("fsIPSecDSCPCopy",             [self._dscpcopy])
        template.setAttribute("fsIPSecExitPolicy",           [self._exitpolicy])
        template.setAttribute("fsIPSecIKEMode",              [self._mode])	
        template.setAttribute("fsIPSecPhase1Encryption",     [self._p1enc])
	template.setAttribute("fsIPSecPhase1Hash",           [self._p1hash])	
        template.setAttribute("fsIPSecPhase1LifeTime",       [self._p1lifetime])
        template.setAttribute("fsIPSecPhase1DHGroup",        [self._p1dhgroup]) 	
        template.setAttribute("fsIPSecPhase1Authentication", [self._p1auth])
        template.setAttribute("fsIPSecPhase1IdentifierType", [self._p1idtype])
        template.setAttribute("fsIPSecPhase2Encryption",     list(self._p2enc_list))        
        template.setAttribute("fsIPSecPhase2LifeTime",       [self._p2lifetime])
        if self._p2pfsgroup != None:
            template.setAttribute("fsIPSecPhase2PFSGroup",       [self._p2pfsgroup])
        template.setAttribute("fsIPSecPhase2Authentication", list(self._p2auth_list))
        if self._dpdaction != None:
            template.setAttribute("fsIPSecDPDAction",       [self._dpdaction])
        if self._dpdinterval != None:
            template.setAttribute("fsIPSecDPDInterval",       [self._dpdinterval]) 
        return template

    ##
    # Validates the command line attributes.
    #
    def validate(self):
        """ Validates the command line attributes.
        """
        if (self._dpdaction == None) and (self._dpdinterval != None):
            raise Exceptions.ParseError("Missmatch in DPD attributes")
        
                    
    ##
    # Validates created template instance and associations.
    #
    # @param template  Complete template instance to be validated.
    #
    def validateInstance(self, template):        
        vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._name)
        # Not much to valide, as long as there are no VPNs connected ...

            
    ##
    # Adds the template object to the LDAP.
    #
    def add(self):
        self.validate()

        # First check if a Template with this name exists. We cannot overwrite is since
        # some VPNs may refer to it and they would be affected by the change of the Template.
#        for n in self._nodelist:
#            temp = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._name, n._node)
            # Allow duplicate templates, still only one instance remains.
            # There shouldn't be any 'loose' VPNs referring to non-existent Template, but
            # to be sure, just check if anyone is referring to this name.
 #           vpn_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecVPN(), self._name, node=n)
 #           if len(vpn_list):
 #               raise Exceptions.ParseError("Template name already referred by a VPN")

        
        # Create template and fill default and mandatory attributes
        template = self.fill(IPSecObject.FSIPSecVPNTemplate())
        template.fillDefaults()
        
        IPSecCreator.add(self, template, 'template')
        
        # Fill the rest here:
        if (self._dpdaction != None):
            template.setAttribute("fsIPSecDPDAction",         [self._dpdaction])
            if (self._dpdaction == "hold"):
                if (self._dpdinterval != None):
                    template.setAttribute("fsIPSecDPDInterval",       [self._dpdinterval])

        # Validate template instance.
        self.validateInstance(template)
        
        # Add object to the LDAP database.
        for n in self._nodelist:
            template.setAttribute("fsIPSecObjectOwner", [n._node])
            template.add(n._node, n._base, force=DuplicatePolicy.ALLOW_DUPLICATE,virtualhost=n._isVirtualHost)


    ##
    # Deletes the globla object from the LDAP database.
    #
    def delete(self):
        # Find the template object to be deleted.
        for n in self._nodelist:
            del_temp = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._name, n._node)
            if del_temp == None:
                raise Exceptions.ObjectNotExistError(msg="Nothing to delete in node %s" % (n._node))
            vpn_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecVPN(), self._name, node=n)
            if len(vpn_list):
                raise IPSecExceptions.ConfigError("Cannot delete a template that is referred by VPN")
        for n in self._nodelist:
            del_temp.delete(n._node, n._base)


##
# IPSec VPN creator
#
class IPSecVPN(IPSecCreator):
    #
    # Constructs VPN object
    #
    # @param name        Name of the VPN.
    # @param template    Name of the template.
    # @param src         Local address of the VPN connection.
    # @param dst         Remote address of the VPN connection.
    # @param ike         IKE version of the VPN.
    # @param mo
    # @param secret      PSK secret for connection.
    # @param cert        Certificate file name.
    # @param certkey     Certifcate key file name.
    # @param cacert
    """ IPSec VPN Creator  Manages the FSIPSecVPN objects. 
    """   
    def __init__(self, name, template=None, src=None, dst=None, ike=None, \
                 secret=None, cert=None,certkey=None,cacert=None, molist=None, vrfId=0):
        self._nodelist   = []
        self._name       = name
        self._ike        = ike
        self._template   = template
        self._family     = None
        if src:
            self._src    = src[0]
            self._family = src[2]
        else:
            self._src    = None
        if dst:
            self._dst    = dst[0]
            self._family = dst[2]
        else:
            self._dst    = None
        self._cert       = cert
        self._certkey    = certkey
        self._cacert     = cacert
        self._secret     = secret
        self._vrfId      = vrfId
        for mo in molist:
            self._nodelist.append(IPSecNode(IPSecObject.FSIPSecVPN(), mo))
    

    ##
    # Fills the command line attributes to the vpn object. Object may be existing one and
    # already contain previously configured attribtes, so also partial filling is possible.
    #
    # @param vpn  Instance where to fill the attributes.
    # @ returns   The filled vpn instance.
    def fill(self, vpn):
        """ Fills the vpn object attributes.
        """
        vpn.setAttribute("fsIPSecVPNName", [self._name])
        vpn.setAttribute("fsIPSecVRFId",   [self._vrfId])
        if self._template != None:
            vpn.setAttribute("fsIPSecVPNTemplateName", [self._template])
        if self._ike != None:
            vpn.setAttribute("fsIPSecVPNIkeVersion", [self._ike])
        if self._family != None:
            vpn.setAttribute("fsIPSecVPNAddressFamily", [self._family])
        if self._src != None:
            vpn.setAttribute("fsIPSecVPNLocalAddress", [self._src])
        if self._dst:
            vpn.setAttribute("fsIPSecVPNRemoteAddress", [self._dst])
        if self._secret != None:
            if isLinSee():
                vpn.setAttribute("fsIPSecVPNSecret", [self._secret])
            else:
                vpn.setAttribute("fsIPSecVPNSecret", "configured")
        if self._cert != None:
            vpn.setAttribute("fsIPSecVPNCertificate", [self._cert])
        if self._certkey != None:
            vpn.setAttribute("fsIPSecVPNCertificateKey", [self._certkey])
        return vpn

    ##
    # Validates the command line attributes.
    #
    def validate(self, node):
        """ Validates command line attributes as such.
        """
        # Local address must exist.
        if not len(findAddresses(node, self._src, self._family)):
            raise IPSecExceptions.ConfigError("Source address not configured in node(s) or IPSec RG")

        # Validate remote address ??

        # Validate the authentication information. If this is modify, there might
        # be only partial attributes in command line.
        if (None != self._secret):
            if (None != self._cert) or (None !=self._certkey):
                raise Exceptions.ParseError("Conflicting authentication attributes")
        else:
            if (None == self._cert) or (None ==self._certkey):
                raise Exceptions.ParseError("Missing authentication attributes")
        
        if isinstance(self, IPSecObject.FSIPSecVPN):
            try:
                IPSecObject.FSIPSecVPN.validate(self)
            except IPSecExceptions.IPSecError, e:
                raise IPSecExceptions.IPSecError("IPSec object %s validation error" % (self._name))
            
        # Check that certificate files are located in the current node, if the default cert dir is used.
        # According to user instructions certificate files are distributed to every node so each of them
        # should be found in this node too, even if the we are configuring some other node. So let's check
        # that files exist.
        if not isLinSee() and None != self._cert:
            for n in self._nodelist:
                key = IPSecObject.FSIPSecGlobal()
                key.setAttribute("fsIPSecVRFId", self._vrfId)    
                ret_list = []
                try:
                    ret_list = getIPSecObjectList(key, node=n._node)                
                except:
                    pass
                if not len(ret_list):
                    raise IPSecExceptions.ConfigError("Couldn't find common object for node %s" % (n._node) )
                if not ret_list[0].getAttribute("fsIPSecGlobalCertificatePath").get():
                    # Using default certificate directory, files should be distributed to local node too. 
                    certFile = IPSecDefaultCertPath+self._cert
                    if not os.path.exists(certFile):
                        raise IPSecExceptions.ConfigError("Certificate file does not exist or not distributed in this node: %s" % (self._cert))
                    certKey = IPSecDefaultCertPath+self._certkey
                    if not os.path.exists(certKey):
                        raise IPSecExceptions.ConfigError("Certificate key file does not exist or not distributed in this node: %s" % (self._certkey))
                else:
                    if Deployment.isSingleNodeDeployment():
                        certFile = ret_list[0].getAttribute("fsIPSecGlobalCertificatePath").get()[0]+self._cert
                        if not os.path.exists(certFile):
                            raise IPSecExceptions.ConfigError("Certificate file does not exist: %s" % (certFile))
                        certKey =  ret_list[0].getAttribute("fsIPSecGlobalCertificatePath").get()[0]+self._certkey
                        if not os.path.exists(certKey):
                            raise IPSecExceptions.ConfigError("Certificate key file does not exist: %s" % (certKey))          
        return

    ##
    # Validates created VPN instance and associations.
    #
    # @param vpn  Complete vpn instance to be validated.
    #.
    def validateInstance(self, vpn):
        """ Validates created VPN instance and associations.
        """
        vrfId = vpn.getAttribute("fsIPSecVRFId").get()[0]
        ike = vpn.getAttribute("fsIPSecVPNIkeVersion").get()[0]
        for n in self._nodelist:
            if not isGlobalSet(n._node, vrfId):
                raise IPSecExceptions.ConfigError("Common settings for node %s does not exist" % (n._node))
            if not isGlobalIke(ike, n._node, vrfId):
                raise IPSecExceptions.ConfigError("VPN IKE version conflicting with Global IKE version")
        
        if isinstance(self, IPSecObject.FSIPSecVPN):
            try:
                IPSecObject.FSIPSecVPN.validate(self)
            except IPSecExceptions.IPSecError, e:
                raise IPSecExceptions.IPSecError("Invalid VPN instance")
        # Check that there are no other VPNs using same peer addresses
        for n in self._nodelist:
            vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), node=n._node)     
            for v in vpn_list:
                if (v.getAttribute("fsIPSecVPNRemoteAddress").get()[0] == vpn.getAttribute("fsIPSecVPNRemoteAddress").get()[0]) and \
                       (v.getAttribute("fsIPSecVPNLocalAddress").get()[0] == vpn.getAttribute("fsIPSecVPNLocalAddress").get()[0]):
                    raise IPSecExceptions.ConfigError("Peer addresses already connected by VPN object %s" % (v.getAttribute("fsIPSecVPNName").get()[0]))
            
        # Check the template that is used. It should exists already, and the IKE version
        # must be same as in this VPN instance. Also, authentication method is defined by template, the
        # data in vpn object must match for that.
        for n in self._nodelist:
            template = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), vpn.getAttribute("fsIPSecVPNTemplateName").get()[0], node=n._node) 
            if template == None:
                raise IPSecExceptions.ConfigError("Template %s does not exist in node %s" % (vpn.getAttribute("fsIPSecVPNTemplateName").get()[0], n._node))
            # If template Phase 1 Identifier type is FQDN, check that it is available for our source address.
            if (template.getAttribute("fsIPSecPhase1IdentifierType").get()[0] == "fqdn"):
                addrInfo=[]
                try:
                    addrInfo = socket.gethostbyaddr(self._src)
                except:
                    pass
                # Don't accept missing FQDN or 'localhost'
                if not len(addrInfo) or addrInfo[0] == None or addrInfo[1][0] == "localhost":
                    raise IPSecExceptions.IPSecError("Failed to solve address %s FQDN required by template %s" % (self._src, self._template))
        
            # Check the IKE version of the vpn object and template
            if (ike != template.getAttribute("fsIPSecVPNIkeVersion").get()[0]):
                raise IPSecExceptions.ConfigError("VPN IKE version %s does not match with template %s " \
                                            % ( self._ike,
                                                template.getAttribute("fsIPSecVPNTemplateName").get()[0]))  
            # Check the authentication information, it is either PSK or certificate files but not both.
            # Also certificate files must exist.
            auth_method = template.getAttribute("fsIPSecPhase1Authentication").get()[0]
            if (auth_method == "secret"):
                if (self._secret == None):
                    raise Exceptions.ParseError("Missing PSK secret required by the Template %s authentication method." \
                                                % (self._template))
                if (self._cacert != None) or (self._certkey != None):
                    raise Exceptions.ParseError("Additional certificate information given for %s authentication method." \
                                                % (self._template))
            else:
                if (auth_method == "certificate"):
                    if (self._cert == None) and (self._cacert == None):
                        raise Exceptions.ParseError("Missing certificate name required for the Template %s authentication method." % (self._template))
                    if (self._cert != None) and (self._certkey == None):
                        raise Exceptions.ParseError("Missing certificate key name required for the Template %s authentication method." % (self._template))
                    if (self._cacert != None) and (self._certkey != None):
                        raise Exceptions.ParseError("Private key not required for CA certificate.")
                    if (self._secret != None):
                        raise Exceptions.ParseError("Additional PSK information given for %s authentication method." \
                                                    % (self._template))
                else:
                     raise Exceptions.ParseError("Missmatch in authentication information of template %s" % (self._template))

        
    ##
    # Adds the vpn object to the database (e.g. LDAP).
    #
    def add(self):
        """ Adds the vpn object to the database (e.g. LDAP).
        """
        # Validate command line attributes
        for n in self._nodelist:
            self.validate(n)
        # Create instance with command line attribtes and validate it
        vpn = self.fill(IPSecObject.FSIPSecVPN())
        vpn.fillDefaults()
        IPSecCreator.add(self, vpn, 'vpn')
        self.validateInstance(vpn)
        
        # If we are in the traget environment, store possible PSK password to the credentials
        # service.        
        for n in self._nodelist:
            if not isLinSee():
                if (self._secret != None) :
                    # Save the PSK to Credential service. Use node as service identification and VPN name as a user.
                    if n._isVirtualHost:
                        if (setCredential(n._virtualHost, self._name, self._secret) == False):
                            raise Exceptions.IPSecException("Failed to save PSK to Credentials service")
                    else:
                        if (setCredential(n._node, self._name, self._secret) == False):
                            raise Exceptions.IPSecException("Failed to save PSK to Credentials service")
            vpn.setAttribute("fsIPSecObjectOwner", [n._node])
            vpn.add(n._node, n._base, virtualhost=n._isVirtualHost)

    ##
    # Modifies a vpn object existing in the LDAP.
    #
    def modify(self):
        self.validate()        

        vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), self._name)
        if not len(vpn_list):
            raise IPSecExceptions.ConfigError("VPN %s object not found!" % (self._name))

        # Fill the modified attributes and validate the result.
        self.fill(vpn_list[0])
        self.validateInstance(vpn_list[0])

        # Check if the local address exists, no further checking so far.
        if (self._src != None):
            if (self._family != None):
                for n in self._nodelist:
                    if not len(findAddresses(n, self._src, self._family)):
                        raise IPSecExceptions.ConfigError("Source address not configured in node(s) or IPSec RG")
        
        
        vpn_list[0].setAttribute("fsIPSecVPNName", [self._name])

        # Check the template that is used. If it exists, the IKE version
        # must be same as in this VPN instance. It is allowed, that template does
        # not exist yet, then we don't just validate values against it.
        if self._template != None:
            self._template = vpn_list[0].getAttribute("fsIPSecVPNTemplateName").get()[0]
            for n in self.nodelist:
                temp_list = getIPSecObjectList(IPSecObject.FSIPSecVPNTemplate(), self._template, node=n._node)
                if not len(temp_list):
                    raise IPSecExceptions.ConfigError("Template %s does not exist in node %s" % (self._template, n._node))
                for template in temp_list:
                    if (self._ike != template.getAttribute("fsIPSecVPNIkeVersion").get()[0]):
                        raise IPSecExceptions.ConfigError("Incompatible IKE version %d found in template %s " % \
                                                          (template.getAttribute("fsIPSecVPNIkeVersion").get()[0],\
                                                           template.getAttribute("fsIPSecVPNTemplateName").get()[0]))
                    auth_method = template.getAttribute("fsIPSecPhase1Authentication").get()[0]
                    if (auth_method == "secret"):
                        if (self._secret == None) and not v.getAttribute("fsIPSecVPNSecret").get()[0] :
                            raise Exceptions.ParseError("Missing secret key required by the Template %s authentication method." % (self._template))
                        if (self._cacert != None) or (self._certkey != None):
                            raise Exceptions.ParseError("Additional certificate information given for %s authentication method." % (self._template))
                        else:
                            if (auth_method == "certificate"):
                                if (self._cert == None) and (self._cacert == None):
                                    raise Exceptions.ParseError("Missing certificate name required for the template %s authentication method." % (self._template))
                                if (self._cert != None) and (self._certkey == None):
                                    raise Exceptions.ParseError("Missing certificate key name required for the template %s authentication method." % (self._template))
                                if (self._cacert != None) and (self._certkey != None):
                                    raise Exceptions.ParseError("Private key not required for CA certificate.")
                                if (self._secret != None):
                                    raise Exceptions.ParseError("Additional PSK information given for %s authentication method." % (template.getAttribute("fsIPSecPhase1Authentication").get()[0]))
        if (self._ike != None):
            vpn_list[0].setAttribute("fsIPSecVPNIkeVersion", [self._ike])
        if (self._family != None):
            vpn_list[0].setAttribute("fsIPSecVPNAddressFamily", [self._family])
        if (self._src != None):
            vpn_list[0].setAttribute("fsIPSecVPNLocalAddress", [self._src])
        if (self._dst):
            vpn_list[0].setAttribute("fsIPSecVPNRemoteAddress", [self._dst])
        if self._secret != None:
            vpn_list[0].setAttribute("fsIPSecVPNSecret", [self._secret])
        if self._cert != None:
            vpn_list[0].setAttribute("fsIPSecVPNCertificate", [self._cert])
        if self._certkey != None:
            vpn_list[0].setAttribute("fsIPSecVPNCertificateKey", [self._certkey])

        # Modify existing LDAP object.
        vpn_list[0].modify(self._node, base=None)

    ##
    # Deletes the vpn object from the LDAP database.
    #        
    def delete(self):
        for n in self._nodelist:
            # If any rules are referring to this VPN, they should be deleted or operation should
            # be refused. Currently we refuse such operation. naming_attribute : [name]}, base
            rule_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecRule(), self._name, n)
            if len(rule_list) > 0:
                raise IPSecExceptions.ConfigError("Cannot delete VPN object (%s) that is referred by rule(s)" % (self._name))

        for n in self._nodelist:
            delvpn = getIPSecObjectList(IPSecObject.FSIPSecVPN(), self._name, n._node)
            if delvpn == None:
                raise Exceptions.ObjectNotExistError(msg="Nothing to delete in node %s" % (n._node))

        # Do it.
        for n in self._nodelist:
            vpn = getIPSecObjectList(IPSecObject.FSIPSecVPN(), self._name, n._node)
            vpn.delete(n._node, n._base)
            # Delete only if LDAP delete is successfull.
            if not isLinSee():
                pwd = delCredentials(n._node, self._name)
        
##
# IPSec Rule Creator
#
class IPSecRule(IPSecCreator):
    #
    # Manages FSIPSecRule objects.
    #
    # @param name         The name of the IPSec rule.
    # @param vpn          The name of the VPN object that this rule is attached to.
    # @param priority     Priority of the rule - 'SPI' - obsole for connections using IKEv2.
    # @param famliy       Address family of the rule addresses.
    # @param src          Local network selector of the rule.
    # @param dst          Remote network selector of the rule.
    # @param srcport      Local port selector of the rule.    # @param dstport      Remote port selector of the rule
    # @param protocol     Protocol selector of the rule
    # @param action       Policy action for the rule.
    # @param mode         Policy mode/type of the IPSec connection (tunnel or transport).
    """ IPSec Rule Creator. Manages the FSIPSecRule objects. 
    """   
    def __init__(self, name, vpn, priority=2000, src=None, dst=None, \
                 srcport=0, dstport=0, protocol=None, action=None, mode=None, molist=None):
        self._nodelist      = []
        self._name          = name
        self._vpn           = vpn
        self._priority      = priority
        if dst:
            self._dstip     = dst[0]
            self._dstlength = dst[1]
            self._family    = dst[2]
            self._dmask_used= dst[3]
        else:
            self._dstip     = None
            self._dstlength = None
        if src:
            self._family    = src[2]
            self._srcip     = src[0]
            self._srclength = src[1]
            self._smask_used= src[3]
        else:
            self._srcip     = None
            self._srclength = None
        self._srcport       = srcport
        self._dstport       = dstport       
        self._protocol      = protocol
        self._mode          = mode
        self._action        = action

        for mo in molist:
            self._nodelist.append(IPSecNode(IPSecObject.FSIPSecRule(), mo))
            
    ##
    # Fills the fule object attributes.
    #
    def fill(self, rule):
        if (self._name != None):
            rule.setAttribute("fsIPSecRuleName", [self._name])        
        if (self._vpn != None):
            rule.setAttribute("fsIPSecRuleVPNName", [self._vpn])
        if (self._priority != None):
            rule.setAttribute("fsIPSecRulePriority", [self._priority])
        else:
            rule.setAttribute("fsIPSecRulePriority", [2000])
        if (self._action != None):
            rule.setAttribute("fsIPSecRulePolicyAction", [self._action])
        if (self._mode != None):
            rule.setAttribute("fsIPSecRulePolicyMode", [self._mode])
        if (self._family != None):
            rule.setAttribute("fsIPSecRuleAddressFamily", [self._family])
        if (self._srcip != None):
            rule.setAttribute("fsIPSecRuleLocalNetwork", [self._srcip]) 
        if ((self._srclength != None and self._srclength != 0) and (self._smask_used)):
            rule.setAttribute("fsIPSecRuleLocalNetworkLength", [self._srclength])
        if (self._dstip != None):
            rule.setAttribute("fsIPSecRuleRemoteNetwork", [self._dstip])
        if ((self._dstlength != None and self._dstlength != 0) and (self._dmask_used)):
            rule.setAttribute("fsIPSecRuleRemoteNetworkLength", [self._dstlength])
        if (self._srcport != None):
            rule.setAttribute("fsIPSecRuleLocalNetworkPort", [self._srcport])
        if (self._dstport != None):
            rule.setAttribute("fsIPSecRuleRemoteNetworkPort", [self._dstport])            
        if (self._protocol != None):
            rule.setAttribute("fsIPSecRuleProtocol", [self._protocol])

        return rule

    ##
    # Compares if rules are duplicates. Kernel considers them as same, but IKE daemons may
    # get confused if there are duplicated SAs configured.
    #
    def isDuplicateRule(self, r):
        # It's a duplicate rule if all the selectors are same. For addresses and masks
        # we have some special cases.
        if (self._action == r.getAttribute("fsIPSecRulePolicyAction").get()[0]) and \
               (self._protocol == int(r.getAttribute("fsIPSecRuleProtocol").get()[0])) and \
               (self._srcip ==  r.getAttribute("fsIPSecRuleLocalNetwork").get()[0]) and \
               (self._dstip ==  r.getAttribute("fsIPSecRuleRemoteNetwork").get()[0]) and \
               (self._srcport == r.getAttribute("fsIPSecRuleLocalNetworkPort").get()[0]) and \
               (self._dstport == r.getAttribute("fsIPSecRuleRemoteNetworkPort").get()[0]):
            if self._action != "clear" and  self._action != "discard":
                if self._mode != r.getAttribute("fsIPSecRulePolicyMode").get()[0]:
                    return False
            # adjust mask variables of this instance ...
            if self._smask_used:
                localLength = self._srclength
            else:
                localLength = None
            if self._dmask_used:
                remoteLength = self._dstlength
            else:
                remoteLength = None
            # Cannot have same rule to same subnets. Subnet with mask /32 conflicts host address.
            # First check if there are identical host addresses.
            if ((not len(r.getAttribute("fsIPSecRuleLocalNetworkLength").get()) and localLength == None)) or \
                   ((not len(r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()) and remoteLength == None)):
                    return True
            else:    
                # If both are subnets ...
                if ((r.getAttribute("fsIPSecRuleLocalNetworkLength").get()) and (localLength != None)) or \
                       ((r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()) and (remoteLength != None)):
                    # ... they must not have same masklen
                    if ((r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0] == remoteLength) and \
                       (r.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0] == localLength)):
                        return True
                # Maybe one of them is a subnet with /mask and other is host address
                if (not len(r.getAttribute("fsIPSecRuleLocalNetworkLength").get()) and (localLength != 32)) and \
                       (not len(r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()) and (remoteLength != 32)):
                    return True
                if (len(r.getAttribute("fsIPSecRuleLocalNetworkLength").get())) and \
                   (len(r.getAttribute("fsIPSecRuleRemoteNetworkLength").get())):
                    if ((r.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0] == 32) and (localLength == None)) and \
                           ((r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0] == 32) and (remoteLength == None)):
                        return True
                else:
                    # Found rule with host address
                    if  (localLength == 32) or (remoteLength == 32):
                        return True
        return False
                              
            
    ##
    # Validates the command line attributes.
    #
    def validate(self):
        """ Validates command line attributes as such.
        """


    ##
    # Validates the instances and associated attributes
    #
    def validateInstance(self, node, rule, vpn):
        # Validate rule attributes against the VPN that must exist.

        # Remote network must not belong to our own networks?
        
        # Compare other rules attached to this VPN.
        rule_list = getIPSecObjectsWithReference(IPSecObject.FSIPSecRule(), self._vpn, node=node)
        for r in rule_list:
            if self.isDuplicateRule(r):
                raise IPSecExceptions.ConfigError("Identical selectors with rule %s" % (r.getAttribute("fsIPSecRuleName").get()[0]))
#            if (rule.getAttribute("fsIPSecRulePolicyMode").get()[0] == "transport") and \
#                   (r.getAttribute("fsIPSecRulePolicyMode").get()[0] == "transport"):
#                raise Exceptions.ParseError("Multiple transport rules for same VPN found.")
            if "fsIPSecRulePriority" in r.getAttributes():
#                if (r.getAttribute("fsIPSecRulePriority").get()[0] == rule.getAttribute("fsIPSecRulePriority").get()[0]):
 #                   if isNetOverlapping(str(r.getAttribute("fsIPSecRuleLocalNetwork").get()[0])+'/'+\
 #                                       str(r.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0]), \
 #                                       str(rule.getAttribute("fsIPSecRuleLocalNetwork").get()[0])+'/'+\
 #                                       str(rule.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0])) or \
 #                       isNetOverlapping(str(r.getAttribute("fsIPSecRuleRemoteNetwork").get()[0])+'/'+\
 #                                       str(r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0]), \
 #                                       str(rule.getAttribute("fsIPSecRuleRemoteNetwork").get()[0])+'/'+\
 #                                       str(rule.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0])):
 #                        raise Exceptions.ParseError("Network selector overlapping.")
 #               else:
                    # Overlapping networks but different priorities. Could make sense, but rules may also
                    # hide each other. Prevent such conflicts.
 #                   if isNetOverlapping(str(r.getAttribute("fsIPSecRuleLocalNetwork").get()[0])+'/'+\
 #                                       str(r.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0]), \
 #                                       str(rule.getAttribute("fsIPSecRuleLocalNetwork").get()[0])+'/'+\
 #                                       str(rule.getAttribute("fsIPSecRuleLocalNetworkLength").get()[0])) or \
 #                       isNetOverlapping(str(r.getAttribute("fsIPSecRuleRemoteNetwork").get()[0])+'/'+\
 #                                       str(r.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0]), \
 #                                       str(rule.getAttribute("fsIPSecRuleRemoteNetwork").get()[0])+'/'+\
 #                                       str(rule.getAttribute("fsIPSecRuleRemoteNetworkLength").get()[0])):
                        # 'Discard' rule action would hide all higher priority rules with overlapping networks.
                if (r.getAttribute("fsIPSecRulePriority").get()[0] > rule.getAttribute("fsIPSecRulePriority").get()[0]) and \
                       (rule.getAttribute("fsIPSecRulePolicyAction").get()[0] == "discard") and \
                       (r.getAttribute("fsIPSecRulePolicyAction").get()[0] != "discard"):
                    raise Exceptions.ParseError("Hiding rule %s" % (r.getAttribute("fsIPSecRuleName").get()[0]) )
                if (r.getAttribute("fsIPSecRulePriority").get()[0] < rule.getAttribute("fsIPSecRulePriority").get()[0]) and \
                       (r.getAttribute("fsIPSecRulePolicyAction").get()[0] == "discard") and \
                       (rule.getAttribute("fsIPSecRulePolicyAction").get()[0] != "discard"):
                    raise Exceptions.ParseError("Hided by the rule %s " % (r.getAttribute("fsIPSecRuleName").get()[0]))
                        
        # Validate policy actions



        # Validate ID types (in phase 2 IP_ADDR and IP_ADDR_SUBNET are supported), both local and remote
        # address must have same ID type, in other words both have to have mask or not mask at all.
        if (len(rule.getAttribute("fsIPSecRuleLocalNetworkLength").get()) and \
           not len(rule.getAttribute("fsIPSecRuleRemoteNetworkLength").get())) or \
           (len(rule.getAttribute("fsIPSecRuleRemoteNetworkLength").get()) and \
           not len(rule.getAttribute("fsIPSecRuleLocalNetworkLength").get())):
            raise IPSecExceptions.ConfigError("Both ource and remote must be addresses or subnets")
        # Must not discard IKE packets - UDP, port 500. Actually kernel does this by default but it does
        # not make sense to configure opposite rule that wouldn't work anyway.
        
        if (rule.getAttribute("fsIPSecRulePolicyAction").get()[0] == "discard") and \
               (rule.getAttribute("fsIPSecRuleProtocol").get()[0] == 17) and \
               ((rule.getAttribute("fsIPSecRuleSrcPort").get()[0] == 500) or \
                (rule.getAttribute("fsIPSecRuleDstPort").get()[0] == 500)):
            raise IPSecExceptions.ConfigError("Cannot discard IKE protocol")
        ike = vpn.getAttribute("fsIPSecVPNIkeVersion").get()[0]
        if (isGlobalIke(1, node._node)):
            if (rule.getAttribute("fsIPSecRulePolicyAction").get()[0] == "clear" or \
                rule.getAttribute("fsIPSecRulePolicyAction").get()[0] == "discard"):
                if (rule.getAttribute("fsIPSecRulePolicyMode").get()):
                    raise IPSecExceptions.ConfigError("Policy mode is not used in association with action type %s " \
                                                % (rule.getAttribute("fsIPSecRulePolicyAction").get()[0]))
            else:    
                if (not rule.getAttribute("fsIPSecRulePolicyMode").get()):
                    raise IPSecExceptions.ConfigError("Policy mode must be defined for action type %s" \
                                                % (rule.getAttribute("fsIPSecRulePolicyAction").get()[0]))
                
        if (isGlobalIke(2, node._node)):
            if (rule.getAttribute("fsIPSecRulePolicyAction").get()[0] != "esp"):
                raise IPSecExceptions.ConfigError("Policy action %s not allowed for IKE version 2 configured for VPN %s " \
                                            % (rule.getAttribute("fsIPSecRulePolicyAction").get()[0], self._vpn))
        # In transport mode VPN address must match with rule local and remote addresses.
        if (rule.getAttribute("fsIPSecRulePolicyMode").get()):
            if (rule.getAttribute("fsIPSecRulePolicyMode").get()[0] == "transport"):
                if (rule.getAttribute("fsIPSecRuleLocalNetwork").get()[0] != vpn.getAttribute("fsIPSecVPNLocalAddress").get()[0] or rule.getAttribute("fsIPSecRuleRemoteNetwork").get()[0] != vpn.getAttribute("fsIPSecVPNRemoteAddress").get()[0]):
                    IPSecExceptions.ConfigError("In transport mode rule addresses must match with VPN addresses.")
        
        
    ##
    # Adds the rule object to the LDAP.
    #
    def add(self):
        """ Adds the rule object to the LDAP.
        """
        # Check if the local network exists, no further checking so far.
        
        # Validate command line attributes
        self.validate()
        
        # Find the VPN entry that is rule refers to. Must exist and be unique.
        for n in self._nodelist:
            vpn_list = getIPSecObjectList(IPSecObject.FSIPSecVPN(), self._vpn, node=n._node)
        
        if vpn_list == None:
            raise IPSecExceptions.ConfigError("VPN object %s does not exist " % (self._vpn))        

        # Create template and fill mandatory attributes
        # Use the defaults from the IPSecObject
        
        # Fill the command line attributes
        rule = self.fill(IPSecObject.FSIPSecRule())
        rule.fillDefaults()
        ike = vpn_list.getAttribute("fsIPSecVPNIkeVersion").get()[0]
        rule.setAttribute("fsIPSecVPNIkeVersion", ike) 
        IPSecCreator.add(self, rule, 'rule')

        # Validate instance and associations.
        for n in self._nodelist:
            self.validateInstance(n, rule, vpn_list)

        # Everything was fine, add the object.
        for n in self._nodelist:
            rule.setAttribute("fsIPSecObjectOwner", [n._node])
            rule.add(n._node, n._base, virtualhost=n._isVirtualHost)

    ##
    # Modifies the existing Rule in the LDAP.
    #
    def modify(self):
        # Validate command line attributes
        self.validate()
        for n in self._nodelist:
            rule = getIPSecObjectList(IPSecObject.FSIPSecRule(), self._name, node=n._node)
            if rule == None:
                raise IPSecExceptions.IPSecError("IPSec rule object &s not found!" % (self._name))
        
            # Find the VPN entry that is rule refers to. Must exist and be unique.
            vpn = getIPSecObjectList(IPSecObject.FSIPSecVPN(), self._vpn, node=n._node)
            if vpn == None:
                raise IPSecExceptions.IPSecError("VPN object %s does not exist " % (self._vpn))     

            # Fill the modified attributes and validate the result.
            self.fill(rule)
        
            self.validateInstance(rule, vpn)

            # Everything ok, apply changes
            rule.modify(self._name, base=n._base)

    ##
    # Deletes the rule object from the LDAP database.
    #        
    def delete(self):
        # Rule shouldn't be referred by anything so we can just delete it if found.
        for n in self._nodelist:
            rule = getIPSecObjectList(IPSecObject.FSIPSecRule(), self._name, n._node)
            if rule==None:
                raise Exceptions.ObjectNotExistError(msg="Nothing to delete in node %s" % (n._node))

            # Do it.
            rule.delete(n._node, n._base)
