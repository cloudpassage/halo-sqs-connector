"""This file contains configuration management functionality."""
import cloudpassage
import os
import re


class ConfigHelper(object):
    """Retrieve configuration settings from environment variables and CLI args.

    Attributes:
        aws_key(str): AWS API key.
        aws_secret(str): AWS API secret.
        aws_default_region(str): AWS region.
        halo_api_key(str): Halo API key.
        halo_api_secret(str): Halo API secret.
        halo_api_hostname(str): Hostname for Halo API.
        halo_module(str): ``events`` or ``scans``
        integration_name(str): Name of this integration
        application_mode(str): ``send`` or ``receive``
        sqs_queue_url(str): URL for SQS queue.
        start_time(str): Timestamp for start of query.
        scan_timeout(int): Timeout for waiting on scans to complete.
    """

    def __init__(self):
        """Call other methods to set instance variables."""
        # Initialize all None
        self.aws_key = None
        self.aws_secret = None
        self.aws_default_region = None
        self.halo_key = None
        self.halo_secret = None
        self.halo_api_hostname = "api.cloudpassage.com"
        self.halo_module = None
        self.application_mode = None
        self.sqs_queue_url = None
        self.start_time = None
        self.scan_timeout = 360
        self.integration_name = "Halo-SQS/%s" % self.get_app_version()
        # Now set according to env.
        self.set_config_vars_from_env()
        self.search_params = self.get_search_params()
        # Make sure we have everything we need.
        self.sanity_check_for_application_mode()
        return

    def sanity_check_for_application_mode(self):
        """Check that all necessary variables are set for application mode."""
        # Generally required settings
        gen_req = {"AWS SQS queue URL": self.sqs_queue_url,
                   "AWS default region": self.aws_default_region,
                   "AWS API key": self.aws_key,
                   "AWS API secret": self.aws_secret,
                   "Application mode": self.application_mode}
        # Required only to send Halo data to SQS queue.
        send_req = {"Halo API key": self.halo_key,
                    "Halo API secret": self.halo_secret,
                    "Halo API hostname": self.halo_api_hostname,
                    "Halo module": self.halo_module,
                    "Scan timeout": self.scan_timeout}
        if self.application_mode not in ["send", "receive"]:
            raise ValueError("Mode must be \"send\" or \"receive\".")
        if self.halo_module not in ["events", "scans"]:
            raise ValueError("Halo module must be \"events\" or \"scans\".")
        # Find missing settings for generall requirements
        missing_settings = [x[0] for x in gen_req if x[1] is None]
        # If we're sending to queue, check for a few more settings.
        if self.application_mode == "send":
            missing_settings.extend([x[0] for x in send_req if x[1] is None])
        # If any required settings are missing, raise ValueError with a
        # meaningful message.
        if missing_settings:
            msg = ("Unable to initialize config.  Missing settings:" %
                   ", ".join(missing_settings))
            raise ValueError(msg)
        if self.application_mode == "send" and self.start_time is None:
            self.start_time = self.get_last_timestamp()
        self.scan_timeout = int(self.scan_timeout)
        return

    def set_config_vars_from_env(self):
        """Set instance variables from environment variables."""
        targets = {"APPLICATION_MODE": "application_mode",
                   "AWS_ACCESS_KEY_ID": "aws_key",
                   "AWS_SECRET_ACCESS_KEY": "aws_secret",
                   "HALO_API_KEY": "halo_key",
                   "HALO_API_SECRET_KEY": "halo_secret",
                   "HALO_API_HOSTNAME": "halo_api_hostname",
                   "HALO_MODULE": "halo_module",
                   "SQS_QUEUE_URL": "sqs_queue_url",
                   "START_TIME": "start_time",
                   "SCAN_TIMEOUT": "scan_timeout"}
        for envvar, varname in targets.items():
            val = os.getenv(envvar)
            if val is not None:
                setattr(self, varname, val)
        return

    def get_last_timestamp(self):
        """Get latest object's timestamp from Halo API."""
        if self.halo_module == "scans":
            url = "/v1/scans?sort_by=created_at.desc&per_page=1"
        elif self.halo_module == "events":
            url = "/v1/events?sort_by=created_at.desc&per_page=1"
        else:
            print("Unrecognized module: %s" % self.halo_module)
        session = cloudpassage.HaloSession(self.halo_key, self.halo_secret,
                                           api_host=self.halo_api_hostname)
        http_helper = cloudpassage.HttpHelper(session)
        timestamp = http_helper.get(url)[self.halo_module][0]["created_at"]
        return timestamp

    @classmethod
    def get_app_version(cls):
        init_loc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "__init__.py")
        with open(init_loc) as initfile:
            raw_init_file = initfile.read()
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        ver = rx_compiled.search(raw_init_file).group(1)
        return ver

    @classmethod
    def get_search_params(cls):
        """Derive search params from env vars."""
        nono_chars = ["\\", ".", "/"]
        env_var = os.getenv("SCAN_FILTER", "")
        if env_var == "":
            return {}
        all_the_nonos = [nono for nono in nono_chars if nono in env_var]
        if all_the_nonos:
            msg = "Invalid chars %s in search params!" % str(all_the_nonos)
            raise ValueError(msg)
        kvs = [x for x in env_var.split(";")]
        retval = {item.split(":")[0]: item.split(":")[1] for item in kvs}
        return retval
