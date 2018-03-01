"""This file contains the top level logic for the halo-sqs-push-pop utility."""

import halosqs
import sys


def main():
    try:
        config = halosqs.ConfigHelper()
    except ValueError as e:
        print("Configuration problem: %s" % e)
        sys.exit(1)
    if config.application_mode == "send":
        runner = halosqs.Sender(config)
    elif config.application_mode == "receive":
        runner = halosqs.Receiver(config)
    runner.run()
    return


if __name__ == "__main__":
    main()
