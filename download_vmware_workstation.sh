#!/bin/bash
#
# VMware Workstation Download Script for Synology NAS
#
# Usage:
#   ./download_vmware_workstation.sh
#
# Requirements:
#   - Docker installed on Synology NAS
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="vmware-downloader"
DOWNLOADS_DIR="/volume1/Public/Applications"

echo "=========================================="
echo "VMware Workstation Automated Downloader"
echo "=========================================="
echo ""
echo "Download directory: $DOWNLOADS_DIR"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed."
    echo "Install Docker via Synology Package Center (Container Manager)."
    exit 1
fi

# Check if we already have the installer
INSTALLER_FILE="$DOWNLOADS_DIR/vmware-workstation.exe"
if [ -f "$INSTALLER_FILE" ]; then
    echo "Existing installer: $(ls -lh "$INSTALLER_FILE" | awk '{print $5, $6, $7, $8}')"
    echo ""
fi

# Build Docker image (--no-cache ensures latest Python script is used)
echo "Building Docker image..."
docker build --no-cache -t "$IMAGE_NAME" "$SCRIPT_DIR"
echo ""

echo "Starting download..."
echo ""

# Run the container with user mapping for correct file ownership
docker run --rm \
    -v "$DOWNLOADS_DIR:/downloads" \
    --user "$(id -u):$(id -g)" \
    "$IMAGE_NAME"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Download completed successfully!"
    echo "Files saved in: $DOWNLOADS_DIR"
    echo "=========================================="
    ls -lh "$INSTALLER_FILE" 2>/dev/null || true
else
    echo ""
    echo "=========================================="
    echo "Download failed."
    echo "=========================================="
fi

exit $EXIT_CODE
