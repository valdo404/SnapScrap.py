"""Infrastructure for SnapScrap.py GCP deployment"""

import base64
import pulumi
from pulumi_gcp import storage, cloudfunctionsv2, pubsub, eventarc, cloudscheduler

# Get configuration
config = pulumi.Config()
gcp_config = pulumi.Config('gcp')

# GCP settings
project = gcp_config.require('project')
region = gcp_config.require('region')

# Storage settings
storage_config = pulumi.Config('storage')
storage_class = storage_config.require('class')

# Function settings
function_config = pulumi.Config('function')
function_runtime = function_config.require('runtime')
function_entry_point = function_config.require('entry_point')
function_memory = function_config.require('memory')
function_timeout = function_config.require_int('timeout')
function_max_instances = function_config.require_int('max_instances')

# Service account
service_account = config.require('service_account')

# Scheduler settings
scheduler_config = pulumi.Config('scheduler')
scheduler_schedule = scheduler_config.require('schedule')
scheduler_timezone = scheduler_config.require('timezone')
scheduler_message = scheduler_config.require('message')

# Storage buckets
snapscrap_bucket = storage.Bucket("snapscrap-bucket",
    name="snapscrap",
    location=region.upper(),
    project=project,
    storage_class=storage_class,
    uniform_bucket_level_access=True,
    force_destroy=True,
)

# Create a valid bucket name from project ID (ensure it's lowercase and contains only valid characters)
function_bucket_name = f"snapscrap-function-source-{project.replace('-', '').lower()}"

function_source_bucket = storage.Bucket("function-source-bucket",
    name=function_bucket_name,
    location=region.upper(),
    project=project,
    storage_class=storage_class,
    uniform_bucket_level_access=True,
    force_destroy=True,
)

# Upload function source ZIP
function_source = storage.BucketObject("function-source",
    name="function.zip",
    bucket=function_source_bucket.name,
    source=pulumi.FileAsset("../../function/function.zip"),  # Path from pulumi directory to function.zip
)

# Pub/Sub topic
snapscrap_topic = pubsub.Topic("snapscrap-topic",
    name="snapscrap",
    project=project,
)

# Cloud Function
snapscrap_function = cloudfunctionsv2.Function("snapscrap-function",
    name="snapscrap",
    location=region,
    project=project,
    build_config=cloudfunctionsv2.FunctionBuildConfigArgs(
        runtime=function_runtime,
        entry_point=function_entry_point,
        source=cloudfunctionsv2.FunctionBuildConfigSourceArgs(
            storage_source=cloudfunctionsv2.FunctionBuildConfigSourceStorageSourceArgs(
                bucket=function_source_bucket.name,
                object=function_source.name
            )
        )
    ),
    service_config=cloudfunctionsv2.FunctionServiceConfigArgs(
        available_memory=function_memory,
        timeout_seconds=function_timeout,
        ingress_settings="ALLOW_ALL",
        all_traffic_on_latest_revision=True,
        max_instance_count=function_max_instances,
        service_account_email=service_account
    ),
    event_trigger=cloudfunctionsv2.FunctionEventTriggerArgs(
        event_type="google.cloud.pubsub.topic.v1.messagePublished",
        pubsub_topic=snapscrap_topic.id,
        retry_policy="RETRY_POLICY_DO_NOT_RETRY",
        service_account_email=service_account,
        trigger_region=region
    ),
    opts=pulumi.ResourceOptions(
        depends_on=[snapscrap_topic]
    ))

# Eventarc trigger
snapscrap_trigger = eventarc.Trigger("snapscrap-trigger",
    name="snapscrap-000452",
    location=region,
    project=project,
    matching_criterias=[{
        "attribute": "type",
        "value": "google.cloud.pubsub.topic.v1.messagePublished"
    }],
    service_account=service_account,
    destination={
        "cloud_run_service": {
            "service": snapscrap_function.service_config.service,
            "region": region,
            "path": "/"
        }
    },
    transport={
        "pubsub": {
            "topic": snapscrap_topic.id
        }
    },
    opts=pulumi.ResourceOptions(
        depends_on=[snapscrap_function, snapscrap_topic]
    ))

# Cloud Scheduler job
snapscrap_scheduler = cloudscheduler.Job("snapscrap-scheduler",
    name="snapscrap",
    schedule=scheduler_schedule,
    time_zone=scheduler_timezone,
    region=region,
    pubsub_target=cloudscheduler.JobPubsubTargetArgs(
        topic_name=snapscrap_topic.id,
        data=base64.b64encode(scheduler_message.encode()).decode()
    ),
    retry_config=cloudscheduler.JobRetryConfigArgs(
        max_retry_duration=scheduler_config.require('max_retry_duration'),
        min_backoff_duration=scheduler_config.require('min_backoff'),
        max_backoff_duration=scheduler_config.require('max_backoff'),
        max_doublings=int(scheduler_config.require('max_doublings'))
    ),
    project=project,
)

# Export values
pulumi.export('bucket_name', snapscrap_bucket.name)
pulumi.export('topic_name', snapscrap_topic.name)
pulumi.export('function_name', snapscrap_function.name)
pulumi.export('trigger_name', snapscrap_trigger.name)
pulumi.export('scheduler_name', snapscrap_scheduler.name)
