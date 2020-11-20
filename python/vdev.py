import os
import subprocess
from time import sleep

"""
    Command line to open a virtual terminal is:
        socat -d -d pty,raw,echo=0 pty,raw,echo=0
    -d -d outputs fatal, error, warning and notice messages
    pty - opens a virtual terminal 
    raw - transfers data with no processing
    echo=0 - does not echo output
"""
vterm = ['socat','-d','-d','-lflog.txt','pty,raw,echo=0','pty,raw,echo=0']

#pactl load-module module-virtual-sink sink_name=VAC_1to2
#pactl load-module module-virtual-sink sink_name=VAC_2to1

#pactl unload-module id given on load-module
#pactl list | grep VAC_1to2 or 35

class VTerm:
    
    def __init__(self):
        self.__vterm = ['socat','-d','-d','-lflog.txt','pty,raw,echo=0','pty,raw,echo=0']
        self.__vtermInst = None
        
    def create(self):
        self.__vtermInst = subprocess.Popen(self.__vterm)
        f = open('log.txt')
        d = f.read()
        f.close()
        n = d.find('/dev/pts/')
        vterm_0 = d[n:n+10]
        n = d.find('/dev/pts/', n+1)
        vterm_1 = d[n:n+10]
        return vterm_0, vterm_1
    
    def destroy(self):
        self.__vtermInst.terminate()

class VAC:
    
    def __init__(self):
        self.__vac_1 = ['pactl', 'load-module', 'module-virtual-sink', 'sink_name=VAC_1to2']
        self.__vac_2= ['pactl', 'load-module', 'module-virtual-sink', 'sink_name=VAC_2to1']
        self.__vacInst_1 = None
        self.__vacInst_2 = None
        self.__vacid_1 = None
        self.__vacid_2 = None
        
    def create(self):
        self.__vacInst_1 = subprocess.Popen(self.__vac_1, stdout=subprocess.PIPE)
        self.__vacInst_2 = subprocess.Popen(self.__vac_2, stdout=subprocess.PIPE)
        self.__vacid_1 = self.__vacInst_1.stdout.read().decode('utf_8').strip()
        self.__vacid_2 = self.__vacInst_2.stdout.read().decode('utf_8').strip()
        print(self.__vacid_1,self.__vacid_2)
        
    def destroy(self):
        subprocess.Popen(['pactl', 'unload-module', self.__vacid_1])
        subprocess.Popen(['pactl', 'unload-module', self.__vacid_2])
    
if __name__ == '__main__':
    #vt = VTerm()
    #print(vt.create())
    #sleep(5)
    #vt.destroy()
    vac = VAC()
    vac.create()
    sleep(5)
    vac.destroy()
    
    