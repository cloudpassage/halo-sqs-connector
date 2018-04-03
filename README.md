# halo-sqs
Stream Halo events and scans to and from Amazon SQS


This tool is intended to be run in a Docker container, but nothing prevents its
operation outside a containerized environment.  All configuration settings are
consumed via environment variables.

Important note: This tool has two operating modes, `send` and `receive`.  
Sending scans or events to SQS does not place the raw scan or event json onto
the queue. Instead, messages are gzipped and base64-encoded before being placed
in SQS.  This is necessary as the size of some Halo scan results can exceed
the maximum message size allowed by SQS.  The tool's `receive` mode is most
useful as an example of how to remove and reconstitute messages from the queue.
For the sake of convenience, the `app/halosqs/utility.py` file contains the
class methods `pack_message()` and `unpack_message()`, which are used in by the
tool to pack and unpack messages before and after queueing, and can easily be
repurposed by your own integration code.  All functionality implemented by the
Utility class (located in `utility.py`) uses only Python built-ins; no external
libraries are required.



### Build:

`docker build -t halo-sqs .`

### Set Environment Variables:

| Variable                | Purpose                                                           |
|-------------------------|-------------------------------------------------------------------|
| APPLICATION_MODE        | Must be set to `send` or `receive`.                               |
| AWS_ACCESS_KEY_ID       | AWS API key. Used for accessing SQS queue.                        |
| AWS_SECRET_ACCESS_KEY   | AWS API secret.                                                   |
| AWS_DEFAULT_REGION      | Regional location of SQS queue.                                   |
| HALO_API_KEY            | API key for Halo. Only required for `send`.                       |
| HALO_API_SECRET_KEY     | API secret for Halo. Only required for `send`.                    |
| HALO_API_HOSTNAME       | Optional. Defaults to `api.cloudpassage.com`                      |
| HALO_MODULE             | Must be set to `events` or `scans`                                |
| SQS_QUEUE_URL           | AWS SQS Queue URL.                                                |
| START_TIME              | ISO8601 timestamp for start of stream.                            |
| SCAN_TIMEOUT            | Optional. Seconds to wait for scan completion.  Default: 360      |
| SCAN_FILTER             | Optional. Set filters for scan retrieval..  See 'Filters', below. |

### Filters:

In environments with high scan volume it may be desirable to filter the scans
sent to SQS by this tool.  This is especially useful as an approach for
multiplexing an extremely voluminous stream of scans across multiple SQS
connectors.

The `SCAN_FILTER` environment variable expects filter keys and values, with a
colon separating the key and value, and a semicolon separating key-value pairs.
For instance, if the desired effect is to only send file integrity scans that
have the `completed_with_errors` status, which means that file integrity
problems were detected, you would set this environment variable:
`SCAN_FILTER="module:fim;status:completed_with_errors"`. For more information
on filtering scans from Halo, see
https://api-doc.cloudpassage.com/help#list-scans

To filter by server group, it is easiest to create API keys in Halo at the
parent group for the assets you wish to target for scan retrieval.

### Run:

* Send events to SQS:

```
    docker run \
      -d \
      -e APPLICATION_MODE=send \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_API_KEY=$HALO_API_KEY \
      -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
      -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -e START_TIME=$START_TIME \
      halo-sqs

```

* Send scans to SQS:

```
    docker run \
      -d \
      -e APPLICATION_MODE=send \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_API_KEY=$HALO_API_KEY \
      -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
      -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
      -e HALO_MODULE=scans \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -e START_TIME=$START_TIME \
      halo-sqs

```

* Receive events from SQS to stdout:

```
    docker run \
      -d \
      -e APPLICATION_MODE=receive \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      halo-sqs

```

* Receive scans from SQS to stdout:

```
    docker run \
      -d \
      -e APPLICATION_MODE=receive \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      halo-sqs

```
