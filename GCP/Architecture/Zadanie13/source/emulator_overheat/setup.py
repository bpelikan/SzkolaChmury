#-------------------------------------------------------------------------
# Copyright (c) Damian Mazurek. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
import time
from logging import log, info, debug, basicConfig, DEBUG, INFO
from emulator import DeviceEmulator

#logging configuration
basicConfig(format='%(asctime)s; %(levelname)s: %(message)s', level=INFO)

# Get env variables
info('Global variables uploaded')
PROJECT_ID = os.environ.get('PROJECT_ID')
TOPIC_NAME = os.environ.get('TOPIC_NAME')
OVERHEAT = int(os.environ.get('OVERHEAT'))
WINDOW_SIZE = int(os.environ.get('WINDOW_SIZE'))
WINDOW_INTERVAL = int(os.environ.get('WINDOW_INTERVAL'))
TIME_INTERVAL = int(os.environ.get('TIME_INTERVAL'))

# Create emulator
info('Creating device emulator')
emulator = DeviceEmulator(PROJECT_ID, TOPIC_NAME)

# Run emulator
emulator.run(OVERHEAT, WINDOW_SIZE, WINDOW_INTERVAL, TIME_INTERVAL)
        

    