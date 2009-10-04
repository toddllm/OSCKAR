import os,sys
sys.path.append('/usr/share/osckar/lib/')
import osckar as o

osckar = o.Osckar()
osckar.connect('localhost',port)
osckar.registerEvent('VM_START_SUCCEEDED')
osckar.registerEvent('VM_BUILD_SUCCEEDED')

def buildVMC(vm_name, install_mirror):
    file = open("/etc/kiosckar/kiosk_template.vmt")
    vmt = file.read()
    file.close()
    vmc = vmt.replace('$VM_NAME', vm_name)
    vmc = vmc.replace('$INSTALL_MIRROR', install_mirror)
    return vmc

def addVM():
    default_install_mirror = "http://archive.ubuntu.com/ubuntu"
    vm_name = raw_input('Enter VM name: ')
    install_mirror = raw_input('Enter alternate install mirror: press enter for default of [' + default_install_mirror + ']')
    install_mirror.strip()
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

def launch(VM):
    f = open(path + VM, 'r')
    osckar.signal('IMPORT_VMC', f.read())
    osckar.signal('START_VM', VM)
    while osckar.waitForEvent('VM_START_SUCCEEDED') != VM:
        pass
    os.system('virt-viewer ' + VM)
