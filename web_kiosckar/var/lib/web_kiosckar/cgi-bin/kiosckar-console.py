#!/usr/bin/python
print "Content-type: text/html\r\n\r\n";

import os,sys
sys.path.append('/usr/share/kiosckar/lib/')
import kiosckar
path='/etc/kiosckar/contracts/'
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = 5000
kiosckar.connect('localhost',port)

print '<form action="formthing.py" method="post">'

VMs = os.listdir(path)
print 'Menu:<br />'
i = 1
for VM in VMs:
    print '<input type="radio" value="%d" name="VMName" /> %s<br />' % (i,VM)
    i += 1

print '<input type="radio" value="%d"  name="VMName" /> %s<br />' % (i,'Add VM')
print '<input type="radio" value="%d"  name="VMName" /> %s<br />' % (i+1,'Exit')
print '<input type="hidden" value="%d" name="i" />' % i
print '<input type="submit" />'
print '<input type="reset" />'
print '</form>'


#    if choice == i+1:
#        sys.exit(0)
#    elif choice == i:
#        default_install_mirror = "http://archive.ubuntu.com/ubuntu"
#        mirror = raw_input('Enter install mirror [' + default_install_mirror + $
#        if mirror.strip() == "":
#            mirror = default_install_mirror
#        choice = raw_input('Enter a VM name:')
#        vm_name = choice.rstrip()
#        kiosckar.addVM(vm_name,mirror)
#    elif choice > 0 and choice < i:
#        kiosckar.destroy(str(choice))
#        kiosckar.launch(path,VMs[choice-1])
#        kiosckar.destroy(str(choice))

#    print ''


