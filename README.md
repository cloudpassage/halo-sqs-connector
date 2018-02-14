# halo-sqs-push-pop
Stream Halo events and scans to and from Amazon SQS


This tool is intended to be run in a Docker container.

## Usage:

### Build:

`docker build -t halo-sqs-push-pop .`

### Set Environment Variables:

| Variable                | Purpose                                         |
|-------------------------|-------------------------------------------------|
| APPLICATION_MODE        | Must be set to `push` or `pop`.                 |
| AWS_ACCESS_KEY_ID       | AWS API key.                                    |
| AWS_SECRET_ACCESS_KEY   | AWS API secret.                                 |
| DROP_DIRECTORY          | Directory on Docker host for storage of output. |
| HALO_API_KEY            | API key for Halo. Only required for push.       |
| HALO_API_SECRET_KEY     | API secret for Halo. Only required for pop.     |
| HALO_API_HOSTNAME       | Optional. Defaults to `api.cloudpassage.com`    |
| HALO_MODULE             | Must be set to `events` or `scans`              |
| SQS_QUEUE_URL           | AWS SQS Queue URL.                              |
| START_TIME              | ISO8601 date for query start.  Defaults to now. |


### Run:

* Push events to SQS:

```
    docker run \
      -d \
      -e APPLICATION_MODE=push \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
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
      -e HALO_API_KEY=$HALO_API_KEY \
      -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
      -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
      -e HALO_MODULE=scans \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -e START_TIME=$START_TIME \
      halo-sqs-push-pop

```

* Pop events from SQS to local storage:

```
    docker run \
      -d \
      -e APPLICATION_MODE=pop \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -v $DROP_DIRECTORY:/var/push-pop/
      halo-sqs-push-pop

```

* Pop scans from SQS to local storage:

```
    docker run \
      -d \
      -e APPLICATION_MODE=pop \
      -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
      -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
      -e HALO_MODULE=events \
      -e SQS_QUEUE_URL=$SQS_QUEUE_URL \
      -v $DROP_DIRECTORY:/var/push-pop/
      halo-sqs-push-pop 

```

### Output format:

The file naming convention for events is `YYYY-MM-DD-halo_events-N.json.gz`
The file naming convention for scans is `YYYY-MM-DD-halo_scans-N.json.gz`

* YYYY-MM-DD is the year, month, and day of the enclosed scans or events.
* Each file will contain a maximum of, 1,000 scan or event objects, ordered
from oldest to newest.
* N indicates the file number.  
* Example: A file named `2018-01-01-halo_scans-2.json.gz` is a gzipped file
which contains scans from New Year's Day, 2018, beginning with the 1,001st
scan for the day.
