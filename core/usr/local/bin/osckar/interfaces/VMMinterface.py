#!/usr/bin/python -Wall

import socket
import os
import xml.dom.minidom
from xml.dom.minidom import Node
import random

import sys
sys.path.append('/usr/local/share/osckar/lib/')
import comm as c

comm = c.Comm()
path = "/etc/VMMInterface/contracts/libvirt/"
if not os.path.isdir(path):
    os.makedirs(path)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', int(sys.argv[1])))
print 'VMM Interface'
print 'connected on port',sys.argv[1]


# These procedures are local to VMM interface
sock.send('regevt' + comm.makeChunk('vmm.start_vm'))
sock.send('regevt' + comm.makeChunk('vmm.shutdown_vm'))
sock.send('regevt' + comm.makeChunk('vmm.destroy_vm'))
sock.send('regevt' + comm.makeChunk('vmm-libvirt.init'))
sock.send('regevt' + comm.makeChunk('vmm.init'))
while 1:
    messageType = sock.recv(6)
    if messageType == 'signal':
        eventName = comm.readChunk(sock)
        eventArgs = comm.readChunk(sock)        
        if eventName == 'vmm.start_vm':
            print "Starting VM", eventArgs
            os.system("virsh define " + path + eventArgs + '.xml')
            returnCode = os.system("virsh start " + eventArgs)
            if returnCode == 0:
                # send an VM_START_SUCCEEDED vmname event
                # osckar.signal("VM_START_SUCCEEDED", eventArgs)
                sock.send('signal' + comm.makeChunk('VM_START_SUCCEEDED') + 
                          comm.makeChunk(eventArgs))
            else:
                 # send VM_START_FAILED vmname event
                # osckar.signal("VM_START_FAILED", eventArgs)
                sock.send('signal' + comm.makeChunk('VM_START_FAILED') + 
                          comm.makeChunk(eventArgs))
        elif eventName == 'vmm.shutdown_vm':
            print "Shutting down VM", eventArgs
            os.system("virsh shutdown " + eventArgs)
        elif eventName == 'vmm.destroy_vm':
            print "Destroying VM", eventArgs
            os.system("virsh destroy " + eventArgs)
        elif eventName == 'vmm-libvirt.init':
            # write the libvirt contract file
            doc = xml.dom.minidom.parseString(eventArgs)
            doc = doc.getElementsByTagName('ruleset')[0]

            libvirtFile = ''

            for line in doc.childNodes:
                libvirtFile += line.toxml()

            # TODO: should grab ruleset id here instead
            vm_name = doc.getElementsByTagName("name")[0].childNodes[0].nodeValue

            outFile = open(path + vm_name + '.xml', 'w')
            #eventArgs is content of libvirt domain configuration file
            outFile.write(libvirtFile)
            outFile.close()           
        elif eventName == 'vmm.init':
            print eventArgs
            doc = xml.dom.minidom.parseString(eventArgs)

            # TODO: should grab ruleset id here instead
            vm_name = doc.getElementsByTagName("name")[0].childNodes[0].nodeValue
            outFile = open(path + vm_name + '.xml', 'w')

            #process contract
            name = doc.getElementsByTagName("name")[0].childNodes[0].data
            memory = doc.getElementsByTagName("memory")[0].getElementsByTagName("default")[0].childNodes[0].nodeValue
            vcpu = len(doc.getElementsByTagName("vcpus"))
            
            disk_paths = []
            cowdisk_paths = []

            for disk in doc.getElementsByTagName('disks')[0].getElementsByTagName('disk'):          
                if disk.getAttribute('type') == "qcow2":
                    disk_paths.append(disk.childNodes[0].data)

            for cowdisk in doc.getElementsByTagName('disks')[0].getElementsByTagName('cowdisk'):          
                if cowdisk.getAttribute('type') == "qcow2":
                    print cowdisk.getAttribute('cowbase')
                    cowtempfile = ''
                    #
                    while cowtempfile == '' or os.path.exists(cowtempfile):
                        cowtempfile = cowdisk.childNodes[0].data + '-' + str(random.randrange(0,32000)) + ".qcow2"
                    #
                    cowpath = "/home/csguest/Desktop/OSCKARcore/interfaces/"
                    print "DEBUG cmd: " + "qemu-img create -f qcow2 -b " + cowdisk.getAttribute('cowbase') + " " + cowtempfile
                    os.system("qemu-img create -f qcow2 -b " + cowdisk.getAttribute('cowbase') + " " + cowtempfile) 
                    disk_paths.append(cowpath + cowtempfile)
         
            bridges = []
            for vnic in doc.getElementsByTagName('vnics')[0].getElementsByTagName('vnic'):
                if vnic.getAttribute('type') == "bridge":
                    if not vnic.hasAttribute('network'):
                        bridges.append("br0")
                    else:
                        bridges.append(vnic.getAttribute('network'))
                else: #type not set, use default
                    bridges.append("br0")
            
            graphics = []
            for graphic in doc.getElementsByTagName('graphics')[0].getElementsByTagName('graphic'):
                graphics.append(graphic.getAttribute('type'))
                    
            #generate output file

            lines = []
            lines.append( "<domain type='kvm'>\n")
            lines.append("<name>" + name + "</name>\n")
            lines.append("<memory>" + memory + "</memory>\n")
            lines.append("<os>\n")
            lines.append("  <type arch=\"x86_64\">hvm</type>\n")
            lines.append("</os>\n")

            lines.append("<devices>")
            lines.append("<emulator>/usr/bin/kvm</emulator>")
       
            for diskpath in disk_paths:
                lines.append("<disk type='file' device='disk'>\n")
                lines.append("<source file='" + diskpath + "'/>\n")
                lines.append("<target dev='hda' bus='ide' />\n")
                lines.append("</disk>\n")
            for bridge in bridges:
                lines.append ("<interface type='bridge'>\n")
                lines.append ("<source bridge='" + bridge + "' />\n")
                lines.append ("</interface>\n")

            for graphic in graphics:
                if graphic == "vnc":
                    lines.append("<graphics type='vnc' port='-1' listen='127.0.0.1' />\n")
                else:
                    lines.append("<graphics type='" + graphic + "' />\n")


            lines.append("</devices>")
            lines.append("</domain>\n")

            for line in lines:
                print line

            outFile.writelines(lines)
            outFile.close()