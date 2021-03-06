"""This file contains functionality to receive Halo data from SQS to stdout."""
from utility import Utility
import boto3
import json
import pprint
import sys


class Receiver(object):
    """Initialize with an instance of ``halosqs.ConfigHelper``."""
    def __init__(self, config):
        self.config = config
        self.sqs = boto3.client('sqs')
        return

    def run(self):
        """Retrieve and unpack Halo data from SQS, and print it to stdout."""
        while True:
            try:
                pprint.pprint(json.loads(self.receive_item_from_sqs()))
            except KeyError:
                print("\nYou reached the end of the data stream!\n\tExiting.")
                sys.exit(0)
        return

    def receive_item_from_sqs(self):
        """Receive one item from SQS."""
        response = self.sqs.receive_message(QueueUrl=self.config.sqs_queue_url,
                                            MaxNumberOfMessages=1)
        message = response["Messages"][0]
        self.sqs.delete_message(QueueUrl=self.config.sqs_queue_url,
                                ReceiptHandle=message["ReceiptHandle"])
        retval = Utility.unpack_message(message["Body"])
        return retval
