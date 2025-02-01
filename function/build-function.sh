#!/bin/bash

# Exit on any error
set -e

echo "=== Building Cloud Function ==="

# Function to clean up on error
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f snapscrap.jar
    if [ "$1" != "0" ]; then
        echo "Build failed!"
        exit $1
    fi
}

# Set up trap for cleanup
trap 'cleanup $?' EXIT

echo "Cleaning previous build artifacts..."
rm -f function.zip snapscrap.jar
rm -rf target/

echo "Building JAR using SBT..."
sbt clean assembly

echo "Creating deployment package..."
# Copy and rename the JAR
cp target/scala-2.13/snapscrap-assembly-0.1.0.jar snapscrap.jar

# Create the ZIP file
zip -j function.zip snapscrap.jar

echo "=== Build Summary ==="
echo "Function package contents:"
unzip -l function.zip

echo "\nBuild successful! Created function.zip"
