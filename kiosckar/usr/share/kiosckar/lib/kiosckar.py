import os,sys
sys.path.append('/usr/share/osckar/lib/')
import osckar as o

osckar = o.Osckar()

def connect(host,port):
    osckar.connect(host,port)
    osckar.registerEvent('VM_START_SUCCEEDED')
    osckar.registerEvent('VM_BUILD_SUCCEEDED')

def buildVMC(vm_name, install_mirror):
    file = open("/etc/kiosckar/kiosk_template.vmt")
    vmt = file.read()
    file.close()
    vmc = vmt.replace('$VM_NAME', vm_name)
    vmc = vmc.replace('$INSTALL_MIRROR', install_mirror)
    return vmc

def addVM(vm_name, install_mirror):
    if(len(install_mirror) == 0):
        install_mirror = default_install_mirror
    vmc = buildVMC(vm_name, install_mirror)
    file = open("/etc/kiosckar/contracts/" + vm_name, "w")
    file.write(vmc)
    file.close()
    osckar.signal('IMPORT_VMC', vmc)
    osckar.signal('BUILD_VM', vm_name)
    while osckar.waitForEvent('VM_BUILD_SUCCEEDED') != vm_name:
        pass

def launch(path,VM):
    f = open(path + VM, 'r')
    vmt = f.read()
    vmc = vmt.replace('$VM_NAME', VM)
    osckar.signal('IMPORT_VMC', vmc)
    osckar.signal('START_VM', VM)
    while osckar.waitForEvent('VM_START_SUCCEEDED') != VM:
        pass
    os.system('virt-viewer ' + VM)

def destroy(VM):
    osckar.signal('DESTROY_VM', VM)
