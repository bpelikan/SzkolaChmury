import uuid
import time
import json
from random import seed, random
from connector import PubSubConnector
from logging import log, info, debug, basicConfig, DEBUG, INFO

class DeviceEmulator:
    def __init__(self, project_id, topic_name):
        self.client = PubSubConnector(project_id, topic_name)
        #create device id
        self.deviceId = uuid.uuid4()

    def send_data(self, data):
        message = data
        return self.client.sendMessage(json.dumps(message), message["deviceid"])

    def run(self, overhead, window_size, window_interval, time_interval ):
        info('Start sending events, window size: %d s',window_size )

        # Run main sending loop
        while True:
            time_to_live = time.time()
            info('Start sending window')

            # Sending in time window
            while (time.time()-time_to_live < window_size):
                seed(time.time())
                # Create data enity
                entity = {"I": 100* random(), "U": 30* random()+210, "Tm": 150* random() + overhead*200* random(), "deviceid": str(self.deviceId), "timestamp": time.time() }
                info('Sending data: %s',str(entity))
                result = self.send_data(entity)
                time.sleep(time_interval)
                info('Entity sended with result %s', str(result))
            
            # Pause sending for specific time
            info('Sending window ended - waiting for next %d s',window_interval)
            overhead = 0
            time.sleep(window_interval)   
