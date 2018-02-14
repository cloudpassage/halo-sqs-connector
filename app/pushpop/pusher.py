"""This file contains functionality for pushing Halo data into SQS."""
from haloevents import HaloEvents
from haloscans import HaloScans
import boto3


class Pusher(object):
    """Initialize with an instance of ``pushpop.ConfigHelper``."""
    def __init__(self, config):
        self.config = config
        self.halo_stream = self.build_halo_stream()
        self.sqs = boto3.client('sqs')
        return

    def build_halo_stream(self):
        """Create Halo data streamer based on settings in ``self.config``."""
        if self.config.halo_module == "events":
            stream = HaloEvents(self.config.halo_key,
                                self.config.halo_secret,
                                api_host=self.config.halo_api_hostname,
                                start_timestamp=self.config.start_time,
                                integration_name=self.config.integration_name)
        else:
            stream = HaloScans(self.config.halo_key,
                               self.config.halo_secret,
                               api_host=self.config.halo_api_hostname,
                               start_timestamp=self.config.start_time,
                               integration_name=self.config.integration_name)
        return stream

    def run(self):
        """Send every item produced by the configured Halo stream to SQS."""
        for item in self.halo_stream:
            self.send_item_to_sqs(item)
        return

    def send_item_to_sqs(self, item):
        """Send one item to SQS.

        Args:
            item(dict): Halo event or scan.
        """
        message_attributes = {"HaloObjectType":
                              {"DataType": "String",
                               "StringValue": self.config.halo_module}}
        self.sqs.send_message(QueueUrl=self.config.sqs_queue_url,
                              MessageAttributes=message_attributes,
                              MessageBody=item)
        return
