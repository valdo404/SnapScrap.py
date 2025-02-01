#!/bin/bash

# Exit on error
set -e

# Load environment variables if .env exists
if [ -f "infra/pulumi/.env" ]; then
    echo "Loading environment variables from .env..."
    export $(cat infra/pulumi/.env | grep -v '^#' | xargs)
fi

# Check required environment variables
if [ -z "$GCP_PROJECT_ID" ] || [ -z "$GCP_SERVICE_ACCOUNT" ] || [ -z "$GCP_REGION" ] || [ -z "$SCHEDULER_MESSAGE" ]; then
    echo "Error: Required environment variables are not set."
    echo "Please set the following variables in infra/pulumi/.env:"
    echo "  - GCP_PROJECT_ID"
    echo "  - GCP_SERVICE_ACCOUNT"
    echo "  - GCP_REGION"
    echo "  - SCHEDULER_MESSAGE"
    exit 1
fi

echo "Building function..."
cd function
./build-function.sh

echo "Deploying infrastructure..."
cd ../infra/pulumi
pulumi up \
    -c gcp:project=${GCP_PROJECT_ID} \
    -c gcp:region=${GCP_REGION} \
    -c snapscrap-infra:service_account=${GCP_SERVICE_ACCOUNT} \
    -c scheduler:message=${SCHEDULER_MESSAGE}
