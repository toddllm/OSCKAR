#!/usr/bin/python -Wall

import xml.dom.minidom
from xml.dom.minidom import Node

import socket
import os
import sys
from string import Template
sys.path.append('/usr/local/share/osckar/lib/')
import comm

class Builder:

    def __init__(self, listenPort=5000, osType='linux', osFlavor='ubuntu', 
                 osVersion='9.04', diskType='disk', diskSize='10240', 
                 diskSparse=True, diskFormat='qcow2', 
                 defaultPartitionType='primary', defaultFileSystem='ext3',
                 hypervisor='kvm', 
                 outputImagePath='/var/lib/osckar/images/',
                 defaultUserPassword='osckar', osArch=''):
        self.listenPort = listenPort
        self.osType = osType
        self.osFlavor = osFlavor
        self.osVersion = osVersion
        self.osArch = osArch
        self.diskType = diskType
        self.diskSize = diskSize
        self.diskSparse = diskSparse
        self.diskFormat = diskFormat
        self.defaultPartitionType = defaultPartitionType
        self.defaultFileSystem = defaultFileSystem

        #set default hypervisor (needed if using vmbuilder script from ubuntu)
        self.hypervisor = hypervisor

        self.outputImagePath = outputImagePath
        
        self.defaultUserPassword = defaultUserPassword

        #create empty disk partitions list
        self.diskParts = []

        #create empty list of users
        self. userList = []

        #create empty sshKeyMaps map
        self.sshKeyMaps = {}

        #create empty lists of packages
        self.packagesToAdd = []
        self.packagesToRemove = []

        #create  my communication object
        self.myComm = comm.Comm()
        


    def connect(self, listenPort=None):

        if listenPort is not None:
            self.listenPort = listenPort

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', self.listenPort))

        print 'Builder Interface'
        print 'connected on port', self.listenPort
    #end function connect


    def registerEvents(self, events):
        for event in events:
            self.sock.send('regevt' + self.myComm.makeChunk(event))
    #end function registerEvents
                           
    def start(self): 
        while 1:
            messageType = self.sock.recv(6)

            eventName = ''
            eventArgs = ''

            if messageType == 'signal':
                eventName = self.myComm.readChunk(self.sock)
                eventArgs = self.myComm.readChunk(self.sock)
        
            if eventName == 'builder.init':
                print 'building VM'
                print 'DEBUG:', eventArgs
                self.contract = xml.dom.minidom.parseString(eventArgs)
                self.parseContract()
                self.doBuild()

    #end function start

    def doBuild(self):
        
        #for now, run vmbuilder as root, a special user would be better
        #TODO: fixme
        self.cmd = 'sudo vmbuilder'
        #self.cmd = 'vmbuilder'
        
        self.cmd += ' ' + self.hypervisor 

        #TODO all this code is vmbuilder specific.
        #Will need to generalize or have if/else to support
        #Other builders such as stacklet, debootstrap, rpm, yast, kickstart
        # sysprep etc.

        #TODO: handle os type for other than linux
        if self.osType == 'linux':
            #TODO: handle os flavor other than ubuntu
            if self.osFlavor == 'ubuntu':
                self.cmd += ' ' + self.osFlavor
            #TODO: handle os version other than 9.04
            if self.osVersion == '9.04':
                self.cmd += ' ' + '--suite="jaunty"'

            if self.osArch != '':
                self.cmd += ' ' + '--arch=' + self.osArch

            #TODO: handle disk type other than "disk"
            #if self.diskType == 'disk':
            #this is the default for kvm, but not xen
                
            #Is disk size supported in vmbuilder?
            #if so, set it to: self.diskSize

            #TODO: handle non-sparse disks
            #this is the default (at least for kvm/qcow2)
            
            #TODO: handle file formats other than qcow2
            #if self.diskFormat == "qcow2"
            #this is the default for kvm, not for xen


            # Specify output dir now, will need to rename to:
            # self.diskFileName after the image is created

            #os.makedirs creates parent directories recurisively
            
            #not needed? vmbuilder creates dir automatically
            # if not os.path.isdir(self.outputImagePath + self.vmid):
            #    os.makedirs(self.outputImagePath + self.vmid)
            self.cmd += ' ' + '--dest=' + self.outputImagePath + self.vmid

            #TODO handle partitions better, 
            # Note, if using vmbuilder, we'll need to 
            # create a "part" (partition table) file and pass it by using 
            # the vmbuilder option --part

            for part in self.diskParts:
                if part.getMountPoint() == "/":
                    self.cmd += ' ' + '--rootsize=' + part.getSize()
                elif part.getFileSystem() == "swap":
                    self.cmd += ' ' + '--swapsize=' + part.getSize()

            
            #TODO handle users better
            # Note, vmbuilder only supports setting up an intial user
            # To support more users, we will need a different solution
            # Stacklet, or our own custom solutions may be necessary
            
            #if vmbuilder, handle first non-root user only
            for user in self.userList:
                if user.getUsername() != "root":
                    self.cmd += ' ' + '--user=' + user.getUsername()
                    self.cmd += ' ' + '--pass=' + user.getPassword()
                    break
            #end for user in usersList
            

            #TODO handle sshkeys better
            # Note, vmbuilder only supports setting up an ssh key for
            # the initial user and root, just like with more users
            # more keys will have to be handled differently

            for (key, value) in self.sshKeyMaps.items():
                if key == "root":
                    self.cmd += ' ' + '--sshkey=' + value
                else: # since only one other user supported by vmbuilder
                    self.cmd += ' ' + '--ssh-user-key=' + value
            #end for (key, value) in self.sshKeyMaps.items():


            self.cmd += ' ' + '--install-mirror=' + self.installmirror
            
            for package in self.packagesToAdd:
                self.cmd += ' ' + '--addpkg=' + package

            for package in self.packagesToRemove:
                self.cmd += ' ' + '--removepkg=' + package

            print 'Building image with command:',self.cmd

            # TODO handle files other than qcow2

            returnCode = os.system(self.cmd)
            if returnCode == 0:
                #expected image file output from vmbuilder
                originalImageFile = self.outputImagePath + str(self.vmid) + '/disk0.qcow2'
                newImageFile = self.outputImagePath + self.vmid + '/' + self.diskFileName
                if os.path.exists(originalImageFile):
                    print 'Renaming image from ' + originalImageFile + ' to ' + newImageFile   
                    os.rename(originalImageFile, newImageFile)
                    print 'Renaming...Done.'
                elif os.path.exists(newImageFile):
                    print 'Using existing image file'
                else:
                    print 'Error, the image: ' + originalImageFile + 'does not exist'
                    #for now, just assume vmbuilder had a problem
                    #TODO, handle more gracefully, support other builders as well
                    print 'Most likely a vmbuilder error'
                    print 'Verify that vmbuilder works correctly on: ' + self.cmd
		    return
            else:
                print 'Error running command: ' + self.cmd
		return

	    self.sock.send('signal' + self.myComm.makeChunk('VM_BUILD_SUCCEEDED') + self.myComm.makeChunk(self.vmid))

    #end doBuild()

    def parseContract(self):

        # parse ruleset tag for id
        self.vmid = self.contract.getElementsByTagName('ruleset')[0].getAttribute('id')

        # parse os info tag
        self.osInfo = self.contract.getElementsByTagName('os')[0]
        if(self.osInfo.hasAttribute('type')):
            self.osType = self.osInfo.getAttribute('type')
        if(self.osInfo.hasAttribute('flavor')):
            self.osFlavor = self.osInfo.getAttribute('flavor')
        if(self.osInfo.hasAttribute('version')):
            self.osVersion = self.osInfo.getAttribute('version')
        if(self.osInfo.hasAttribute('arch')):
            self.osArch = self.osInfo.getAttribute('arch')
        
        
        # parse disk tag
        self.diskInfo = self.contract.getElementsByTagName('disk')[0]
        if(self.diskInfo.hasAttribute('type')):
            self.diskType = self.diskInfo.getAttribute('type')
        if(self.diskInfo.hasAttribute('size')):
            self.diskSize = self.diskInfo.getAttribute('size')
        if(self.diskInfo.hasAttribute('sparse')):
            if(self.diskInfo.getAttribute('sparse') == "true"):
                self.diskSparse = True
        if(self.diskInfo.hasAttribute('format')):
            self.diskFormat = self.diskInfo.getAttribute('format')

        self.diskFileName = self.diskInfo.childNodes[0].nodeValue
        
        # parse partitions tags
        self.diskPartitions = self.contract.getElementsByTagName('partitions')[0]
        for part in self.diskPartitions.getElementsByTagName('partition'):
            # parse each individual partition tag
            
            # create an partition object to hold each partition tag element
            partition = self.Partition()
            if part.hasAttribute('type'):
                partition.setType(part.getAttribute('type'))
            else:
                partition.setType(self.defaultPartionType)
            if part.hasAttribute('filesystem'):
                partition.setFileSystem(part.getAttribute('filesystem'))
            else:
                partition.setFileSystem(self.defaultFileSystem)
            if part.hasAttribute('bootable'):
                partition.setBootable(part.getAttribute('bootable'))

            # set required partition fields
            partition.setMountPoint(part.getAttribute('mountpoint'))
            partition.setSize(part.getAttribute('size'))
            partition.setNumber(part.childNodes[0].nodeValue)
            
            # add partition to partition list
            self.diskParts.append(partition)
        #end for part in self.diskPartitions.getElementByTagname('partition'):

        # parse user tags
        self.users = self.contract.getElementsByTagName('users')[0]
        for user in self.users.getElementsByTagName('user'):
            # parse each individual user tag
            
            aUser = self.User()
            if(user.hasAttribute('logindisabled')):
                aUser.setLoginDisabled(user.getAttribute('logindisabled'))
            if(user.hasAttribute('password')):
                aUser.setPassword(user.getAttribute('password'))
            else:
                aUser.setPassword(self.defaultUserPassword)
            if(user.hasAttribute('groups')):
                groups = user.getAttribute('groups')
                groupList = groups.split(',')
                for group in groupList:
                    aUser.addToGroup(group)
            #set username
            aUser.setUsername(user.childNodes[0].nodeValue)
            #add user to user list
            self.userList.append(aUser)
        #end for user in self.users.getElementsByTagName('user'):
            
            
        # parse sshkey tags
        sshkeysElement = self.contract.getElementsByTagName('sshkeys')
        if len(sshkeysElement) > 0:
            self.sshkeys = sshkeysElement[0]
            for sshkey in self.sshkeys.getElementsByTagName('sshkey'):
                # parse each individual sshkey tag
                self.sshKeyMaps[sshkey] = sshkey.childNodes[0].nodeValue
             

        # parse packages tags
        self.packages = self.contract.getElementsByTagName('packages')[0]
        for package in self.packages.getElementsByTagName('package'):
            # parse each individual package tag
            if package.getAttribute('action') == "add":
                self.packagesToAdd.append(package.getAttribute("name"))
            elif package.getAttribute('action') == "remove":
                self.packagesToRemove.append(package.getAttribute("name"))
                                          
        # parse installmirror tag
        #TODO fixme if self.contract.hasTagName('installmirror'):
        self.installmirror = self.contract.getElementsByTagName('installmirror')[0].childNodes[0].nodeValue
            
    class Partition:

        def __init__(self, bootable=False):
            self.bootable = bootable
            
        def setNumber(self, number):
            self.number = number

        def getNumber(self):
            return self.number

        def setType(self, type):
            self.type = type
            
        def getType(self):
            return self.type

        def setFileSystem(self, fileSystem):
            self.fileSystem = fileSystem

        def getFileSystem(self):
            return self.fileSystem

        def setMountPoint(self, mountPoint):
            self.mountPoint = mountPoint

        def getMountPoint(self):
            return self.mountPoint

        def setSize(self, size):
            self.size = size

        def getSize(self):
            return self.size

        def setBootable(self, bootable):
            self.bootable = bootable

        def getBootable(self):
            return self.bootable

    #end class partition

    class User:
        def __init__(self):
            self.loginDisabled = False
            self.groups = []

        def setLoginDisabled(self, loginDisabled):
            self.loginDisabled = loginDisabled
                
        def getLoginDisabled(self):
            return self.loginDisabled
            
        def setUsername(self, username):
            self.username = username
            
        def getUsername(self):
            return self.username

        def setPassword(self, password):
            self.password = password
            
        def getPassword(self):
            return self.password
        
        def addToGroup(self, group):
            self.groups.append(group)
            
        def setGroups(self, groups):
            self.groups = groups

        def getGroups(self):
            return self.groups
    
    # end class User


#end class Builder


listenPort = int(sys.argv[1])

myBuilder = Builder(listenPort)
myBuilder.connect()
#pass list of eventes to register for
myBuilder.registerEvents(("builder.init",))
myBuilder.start()
