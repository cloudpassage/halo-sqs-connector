"""This file contains the top level logic for the halo-sqs-push-pop utility."""

import pushpop
import sys


def main():
    try:
        config = pushpop.ConfigHelper()
    except ValueError as e:
        print("Configuration problem: %s" % e)
        sys.exit(1)
    if config.application_mode == "push":
        runner = pushpop.Pusher(config)
    elif config.application_mode == "pop":
        runner = pushpop.Popper(config)
    runner.run()
    return


if __name__ == "__main__":
    main()
