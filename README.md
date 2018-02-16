# halo-sqs-push-pop
Stream Halo events and scans to and from Amazon SQS


This tool is intended to be run in a Docker container, but nothing prevents its
operation outside a containerized environment.  All configuration settings are
consumed via environment variables.

Important note: This tool has two operating modes, `push` and `pop`.  Pushing
scans or events to SQS does not place the raw scan or event json onto the
queue.  Instead, messages are gzipped and base64-encoded before being placed
in SQS.  This is necessary as the size of some Halo scan results can exceed
the maximum message size allowed by SQS.  The tool's `pop` mode is most useful
as an example of how to remove and reconstitute messages from the queue. For
the sake of convenience, the `app/pushpop/utility.py` file contains the class
methods `pack_message()` and `unpack_message()`, which are used in by the tool
to pack and unpack messages before and after queueing, and can easily be
repurposed by your own integration code.  All functionality implemented by the
Utility class (located in `utility.py`) uses only Python built-ins; no external
libraries are required.



### Build:

`docker build -t halo-sqs-push-pop .`

### Set Environment Variables:

| Variable                | Purpose                                         |
|-------------------------|-------------------------------------------------|
| APPLICATION_MODE        | Must be set to `push` or `pop`.                 |
| AWS_ACCESS_KEY_ID       | AWS API key.                                    |
| AWS_SECRET_ACCESS_KEY   | AWS API secret.                                 |
| AWS_DEFAULT_REGION      | Region for SQS queue.                           |
| HALO_API_KEY            | API key for Halo. Only required for push.       |
| HALO_API_SECRET_KEY     | API secret for Halo. Only required for pop.     |
| HALO_API_HOSTNAME       | Optional. Defaults to `api.cloudpassage.com`    |
| HALO_MODULE             | Must be set to `events` or `scans`              |
| SQS_QUEUE_URL           | AWS SQS Queue URL.                              |
| START_TIME              | ISO8601 timestamp for start of stream.          |


### Run:

* Push events to SQS:

```
    docker run \
      -d \
      -e APPLICATION_MODE=push \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_API_KEY=$HALO_API_KEY \
      -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
      -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -e START_TIME=$START_TIME \
      halo-sqs-push-pop

```

* Push scans to SQS:

```
    docker run \
      -d \
      -e APPLICATION_MODE=push \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_API_KEY=$HALO_API_KEY \
      -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
      -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
      -e HALO_MODULE=scans \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -e START_TIME=$START_TIME \
      halo-sqs-push-pop

```

* Pop events from SQS to stdout:

```
    docker run \
      -d \
      -e APPLICATION_MODE=pop \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      halo-sqs-push-pop

```

* Pop scans from SQS to stdout:

```
    docker run \
      -d \
      -e APPLICATION_MODE=pop \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      halo-sqs-push-pop

```
