#!/usr/bin/env python
#
# antcontrol.py
#
# Controller API for the Antenna Switch application
# 
# Copyright (C) 2015 by G3UKB Bob Cowdery
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
import socket
import threading
import traceback

# Application imports
from commondefs import *

"""
Controller API
"""
class AntControl :
    
    def __init__(self, network_params, relay_state, callback):
        """
        Constructor
        
        Arguments:
        
            network_params   --  [ip, port] address of Arduino
            relay_state      --  initial relay state
            callback         --  status and progress callback
        """
        
        if len(network_params) == 0 or network_params[0]== None or network_params[1]== None:
            # Not configured yet
            self.__ip = None
            self.__port = None
            self.__ready = False
        else:
            self.__ip = network_params[0]
            self.__port = int(network_params[1])
            self.__ready = True
        
        # Callback here with progress, SWR, completion etc
        self.__callback = callback
        # Current state of relays
        self.__relay_state = relay_state
        # Socket
        self.__sock =  None
        
        self.__online = False
        if self.__ready:
            # Create UDP socket
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Check connectivity
            if self.__ping():
                self.__online = True
                # Set the relays according to the state
                if self.__relay_state != None:
                    self.__init_relays()
                    
        # Sync event
        self.__evnt = threading.Event()
        self.__evnt.set()

    # API =============================================================================================================           
    def resetParams(self, ip, port, relay_state = None):
        """
        Parameters (may) have changed
        
        Arguments:
        
            ip          --  IP address of Arduino
            port        --  port address for Arduino
            relay_state --  current relay state
            
        """
        
        self.__ip = ip
        self.__port = int(port)
        self.__ready = True
        if self.__sock != None:
           self.__sock.close()
        # Create UDP socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the relays according to the state
        if self.__ping():
            self.__online = True
            if relay_state != None:
                self.__relay_state = relay_state
                for relay_id, state in self.__relay_state.items():
                    self.set_relay(relay_id, state)
    
    def set_relay(self, relay_id, switch_to):
        """
        Parameters (may) have changed
        
        Arguments:
        
            relay_id    --  1-6
            switch_to   --  RELAY_ON|RELAY_OFF
        """
        
        if not self.__ready:
            self.__callback('failure: no network params!')
            return
        if self.__online:
            self.__evnt.wait()
            if switch_to == RELAY_ON:
                self.__send(str(relay_id) + 'e')
            else:
                self.__send(str(relay_id) + 'd')
            self.__evnt.clear()
            self.__evnt.set()
        else:
            self.__callback('failure: offline!')
    
    def reset_relays(self, ):
        """ Set all relays de-energised """
        
        if self.__ready:
            for relay_id in range(1,7):
                self.set_relay(relay_id, RELAY_OFF)
    
    def is_online(self, relay_state):
        """
        If offline try and get up online, return online state
        
        Arguments:
            relay_state --  current state to use if we move to online
            
        """
        
        if self.__ready:
            if self.__ping():
                if not self.__online:
                    # Moved to online state
                    self.__online = True
                    if relay_state != None:
                        self.__relay_state = relay_state
                        self.__init_relays()
                return True
            else:
                # Now, or still offline
                self.__online = False
                return False        
        else:
            # Not initialised
            return False
        
    # Helpers =========================================================================================================    
    # Init to current state
    def __init_relays(self):
       
        for relay_id, state in self.__relay_state.items():
            if state == RELAY_ON:
                self.__send(str(relay_id) + 'e')
            else:
                self.__send(str(relay_id) + 'd')
            
    # Send relay command    
    def __send(self, command):
        
        self.__sock.sendto(bytes(command, "utf-8"), (self.__ip, self.__port))
    
    # Do a ping exchange
    def __ping(self):
        
        if not self.__ready:
            return False
        
        try:
            self.__sock.sendto(bytes('ping', "utf-8"), (self.__ip, self.__port))
            self.__sock.settimeout(2.0)
            data, addr = self.__sock.recvfrom(1024) # buffer size is 1024 bytes
            return True
        except socket.timeout:
            # Server didn't respond
            return False
        except Exception as e:
            # Something went wrong
            return False
        