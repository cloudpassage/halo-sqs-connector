"""This file contains functionality to pop Halo data from SQS to stdout."""
from utility import Utility
import boto3
import json
import pprint
import sys


class Popper(object):
    """Initialize with an instance of ``pushpop.ConfigHelper``."""
    def __init__(self, config):
        self.config = config
        self.sqs = boto3.client('sqs')
        return

    def run(self):
        """Retrieve and unpack Halo data from SQS, and print it to stdout."""
        while True:
            try:
                pprint.pprint(json.loads(self.pop_item_from_sqs()["Body"]))
            except KeyError:
                print("\nYou reached the end of the data stream!\n\tExiting.")
                sys.exit(0)
        return

    def pop_item_from_sqs(self):
        """Pop one item from SQS."""
        response = self.sqs.receive_message(QueueUrl=self.config.sqs_queue_url,
                                            MaxNumberOfMessages=1)
        message = response["Messages"][0]
        self.sqs.delete_message(QueueUrl=self.config.sqs_queue_url,
                                ReceiptHandle=message["ReceiptHandle"])
        return Utility.unpack_message(message)
