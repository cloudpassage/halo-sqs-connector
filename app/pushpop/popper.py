"""This file contains functionality to pop Halo data from SQS to stdout."""
import boto3
import pprint


class Popper(object):
    """Initialize with an instance of ``pushpop.ConfigHelper``."""
    def __init__(self, config):
        self.config = config
        self.sqs = boto3.client('sqs')
        return

    def run(self):
        """Send every item produced by the configured Halo stream to SQS."""
        while True:
            pprint.pprint(self.pop_item_from_sqs()["body"])
        return

    def pop_item_from_sqs(self):
        """Pop one item from SQS."""
        response = self.sqs.receive_message(QueueUrl=self.config.sqs_queue_url,
                                            MaxNumberOfMessages=1)
        message = response["messages"][0]
        self.sqs.delete_message(QueueUrl=self.config.sqs_queue_url,
                                ReceiptHandle=message["ReceiptHandle"])
        return message
