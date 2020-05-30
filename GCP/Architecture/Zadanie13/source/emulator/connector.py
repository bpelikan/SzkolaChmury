from google.cloud import pubsub_v1

class PubSubConnector:
    def __init__(self, project_id, topic_name):
        self.project_id = project_id
        self.topic_name = topic_name
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name)

    def sendMessage(self, message, deviceId):
        data = message.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data=data, deviceId = deviceId )
        return future.result()
