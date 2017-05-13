#!/usr/bin/env python
#
# commondefs.py
#
# Common defs for the loop control, antenna control and CAT for use by WSPRController
# 
# Copyright (C) 2017 by G3UKB Bob Cowdery
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

# ============================================================================
# Antenna Control

RELAY_OFF = 'relayoff'
RELAY_ON = 'relayon'

# Loop Controller ==========
# Buffer size
RECEIVE_BUFFER = 512
# Timeout for responses
CONTROLLER_TIMEOUT = 20
# Timeout for responses and events
CONTROLLER_TIMEOUT = 1
# Arduino event port on which we listen
EVENT_PORT = 8889
# Select analog reference
INTERNAL = 'internal'
EXTERNAL = 'external'

# ============================================================================
# CAT

# Settings
CAT_SETTINGS = 'catsettings'
NETWORK = 'network'
SERIAL = 'serial'
SELECT = 'select'
VARIANT = 'variant'
CAT_UDP = 'catudp'
CAT_SERIAL = 'catserial'

# Index into comms parameters
IP = 0
PORT = 1
COM_PORT = 0
BAUD_RATE = 1

# CAT variants
FT_817ND = 'FT-817ND'
IC7100 = 'IC7100'
CAT_VARIANTS = [FT_817ND, IC7100]
YAESU = 'YAESU'
ICOM = 'ICOM'

# ============================================================================
# Constants used in command sets
REFERENCE = 'reference'
MAP = 'map'
CLASS = 'rigclass'
SERIAL = 'serial'
COMMANDS = 'commands'
MODES = 'modes'
PARITY = 'parity'
STOP_BITS = 'stopbits'
TIMEOUT = 'timeout'
READ_SZ = 'readsz'
LOCK_CMD = 'lockcmd'
LOCK_SUB = 'locksub'
LOCK_ON = 'lockon'
LOCK_OFF = 'lockoff'
MULTIFUNC_CMD = 'multifunccmd'
MULTIFUNC_SUB = 'multifuncsub'
PTT_ON = 'ptton'
PTT_OFF = 'pttoff'
SET_FREQ_CMD = 'setfreqcmd'
SET_FREQ_SUB = 'setfreqsub'
SET_FREQ = 'setfreq'
SET_MODE_CMD = 'setmodecmd'
SET_MODE_SUB = 'setmodesub'
SET_MODE = 'setmode'
GET_FREQ_CMD = 'getfreqcmd'
GET_FREQ_SUB = 'getfreqsub'
GET_MODE_CMD = 'getmodecmd'
GET_MODE_SUB = 'getmodesub'
FREQ_MODE_GET = 'freqmodeget'
RESPONSES = 'responses'

ACK = 'ack'
NAK = 'nak'

# ============================================================================
# Constants used in command sets and to be used by callers for mode changes
MODE_LSB = 'lsb'
MODE_USB = 'usb'
MODE_CW = 'cw'
MODE_CWR = 'cwr'
MODE_AM = 'am'
MODE_FM = 'fm'
MODE_DIG = 'dig'
MODE_PKT = 'pkt'
MODE_RTTY = 'rtty'
MODE_RTTYR = 'rttyr'
MODE_WFM = 'wfm'
MODE_DV = 'dv'

# ============================================================================
# CAT command set to be used by callers
CAT_LOCK = 'catlock'
CAT_PTT = 'catptt'
CAT_FREQ_SET = 'catfreqset'
CAT_MODE_SET = 'catmodeset'
CAT_FREQ_GET = 'catfreqget'
CAT_MODE_GET = 'catmodeget'
