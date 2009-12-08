#!/usr/bin/python
print "Content-type: text/html\r\n\r\n";

import os,sys
sys.path.append('/usr/share/kiosckar/lib/')
import kiosckar
import cgi
path='/etc/kiosckar/contracts/'
if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = 5000
kiosckar.connect('localhost',port)

VMs = os.listdir(path)
i = 1
for VM in VMs:
    i += 1

form = cgi.FieldStorage()
choice = int(form["VMName"].value)
if int(form["i"].value) != i:
 print 'Error'
elif choice == i+1:
  sys.exit(0)
elif choice == i:
  print 'Feature not yet implemented'
elif choice > 0 and choice < i:
  print 'destroying'
  kiosckar.destroy(str(choice))
  print 'launching'
  kiosckar.launch(path,VMs[choice-1],False)

print ''

