# SnapScrap Cloud Function

This is a Google Cloud Function written in Scala that handles Pub/Sub messages. The function is triggered by Cloud Scheduler and logs the received message.

## Building

To build the function, run:

```bash
sbt clean assembly
```

This will create a JAR file in `target/scala-2.13/snapscrap-assembly-0.1.0.jar`.

## Configuration

The function expects a Pub/Sub message with base64 encoded data. The message content is configured in the Pulumi infrastructure code.

## Development

The project uses:
- Scala 2.13.10
- SBT for build management
- Google Cloud Functions Framework
- Google Cloud Events for Pub/Sub
- Gson for JSON parsing
- SLF4J and Logback for logging

## Infrastructure

The function is deployed using Pulumi with the following configuration:
- Memory: 256MB
- Timeout: 60 seconds
- Runtime: Java 17
- Region: europe-west1
- Schedule: Every 30 minutes
