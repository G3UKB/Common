#!/usr/bin/env python
#
# vdev.py
#
# Linux virtual port control
# 
# Copyright (C) 2020 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#

# System imports
import os, sys
import subprocess
from time import sleep
import traceback
import signal

"""
    This command line module creates virtual serial ports
    and virtual audio connections.
    One pair or each is created. They are destroyed when
    the application terminates.
    
    =========================================================
    Command line to create a pair of virtual serial ports is:
        socat -d -d pty,raw,echo=0 pty,raw,echo=0
        
    -d -d outputs fatal, error, warning and notice messages
    -lf path - logs to a file rather than stderr
    pty - opens a virtual terminal 
    raw - transfers data with no processing
    echo=0 - does not echo output
    
    The command does not return until until terminated. As we cannot
    get the device names until the process exits we log to a file and
    extract the device names for use in communicating applications.
    
    =========================================================
    Command line to create a pair of virtual audio cables is:
        pactl load-module module-virtual-sink sink_name=VAC_1to2
        pactl load-module module-virtual-sink sink_name=VAC_2to1
    
    This uses PulseAudio to create two sinks VAC_1to2 and VAC_2to1. Any
    name can be used.
    
    The command return immediately after creation returning the device ID.
    The ID is required to destroy the connections.
"""

#======================================================================================
"""
    Virtual serial ports
"""
class VTerm:
    
    """
        Constructor
    """
    def __init__(self):
        # Command line
        self.__vterm = ['socat','-d','-d','-lflog.txt','pty,raw,echo=0','pty,raw,echo=0']
        # Instance
        self.__vtermInst = None
    
    """
        Create connections
    """
    def create(self):
        # Run process
        self.__vtermInst = subprocess.Popen(self.__vterm)
        # Open log file and extract device names
        f = open('log.txt')
        d = f.read()
        f.close()
        n = d.find('/dev/pts/')
        vterm_0 = d[n:n+10]
        n = d.find('/dev/pts/', n+1)
        vterm_1 = d[n:n+10]
        return vterm_0, vterm_1
    
    """
        Destroy connections
    """
    def destroy(self):
        # Terminate process
        self.__vtermInst.terminate()

#======================================================================================
"""
    Virtual audio cable
"""
class VAC:
    
    # Constructor
    def __init__(self):
        # Command lines
        self.__vac_0 = ['pactl', 'load-module', 'module-virtual-sink', 'sink_name=VAC_1to2']
        self.__vac_1= ['pactl', 'load-module', 'module-virtual-sink', 'sink_name=VAC_2to1']
        # Instances
        self.__vacInst_0 = None
        self.__vacInst_1 = None
        self.__vacid_0 = None
        self.__vacid_1 = None
    
    """
        Create connections
    """    
    def create(self):
        # Run processes
        self.__vacInst_0 = subprocess.Popen(self.__vac_0, stdout=subprocess.PIPE)
        self.__vacInst_1 = subprocess.Popen(self.__vac_1, stdout=subprocess.PIPE)
        # Read device ID's
        self.__vacid_0 = self.__vacInst_0.stdout.read().decode('utf_8').strip()
        self.__vacid_1 = self.__vacInst_1.stdout.read().decode('utf_8').strip()
        return self.__vacid_0,self.__vacid_1
    
    """
        Destroy connections
    """
    def destroy(self):
        # Destroy using the returned ID's
        subprocess.Popen(['pactl', 'unload-module', self.__vacid_0])
        subprocess.Popen(['pactl', 'unload-module', self.__vacid_1])

#======================================================================================
# Main code
vt = None
vac = None

def tidyExit(signal, frame):
    try:
        vt.destroy()
        vac.destroy()
        print("/nVirtual devices destroyed.")
    except Exception as e:
        print ('Exception on exit [%s][%s]' % (str(e), traceback.format_exc()))
    sys.exit(0)
        
def main():
    global vt
    global vac
    
    try:
        # Create instances
        vt = VTerm()
        vac = VAC()
        # Create devices
        vterm_0, vterm_1 = vt.create()
        vacid_0, vacid_1 = vac.create()
        # Output messages
        print("Created virtual serial ports: %s, %s" % (vterm_0, vterm_1))
        print("Created virtual audio cables: %s, %s" % (vacid_0, vacid_1))
        
        # Wait for termination
        signal.signal(signal.SIGINT, tidyExit)
        print("Ctrl+C to exit")
        signal.pause()
        
    except Exception as e:
        print ('Exception on create [%s][%s]' % (str(e), traceback.format_exc()))
 
# Entry point   
if __name__ == '__main__':
    main()
    
    
    