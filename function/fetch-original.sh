#!/bin/bash

# Clean up any existing files
rm -f original-function.zip function-source.zip

# Fetch the original function from GCS
gsutil cp gs://gcf-v2-sources-342376591000-europe-west1/snapscrap/function-source.zip original-function.zip

echo "Original function downloaded as original-function.zip"
unzip -l original-function.zip
