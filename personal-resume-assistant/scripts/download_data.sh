#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CV_DIR="$SCRIPT_DIR/../data/CVs"
WGET_FILE="$SCRIPT_DIR/wget_cv.txt"

# Create CVs directory if it doesn't exist
mkdir -p "$CV_DIR"

# Check if wget_cv.txt exists
if [ ! -f "$WGET_FILE" ]; then
    echo "Error: wget_cv.txt file not found in $SCRIPT_DIR"
    exit 1
fi

# Counter for naming files
counter=1

echo "Starting PDF download process..."
echo "Target directory: $CV_DIR"
echo "Reading URLs from: $WGET_FILE"
echo ""

# Read each line from wget_cv.txt
while IFS= read -r url; do
    # Skip empty lines
    if [ -z "$url" ]; then
        continue
    fi
    
    # Remove any carriage return characters
    url=$(echo "$url" | tr -d '\r')
    
    echo "Processing URL $counter: $url"
    
    # Generate filename
    filename="CV_$counter.pdf"
    filepath="$CV_DIR/$filename"
    
    # Download the file
    echo "Downloading to: $filename"
    if wget -q --show-progress -O "$filepath" "$url"; then
        echo "✓ Successfully downloaded: $filename"
        
        # Verify it's a PDF file by checking the header
        if file "$filepath" | grep -q "PDF"; then
            echo "✓ Confirmed as PDF format"
        else
            echo "⚠ Warning: Downloaded file may not be in PDF format"
            # Optionally rename with correct extension based on file type
            file_type=$(file -b --mime-type "$filepath")
            echo "  Detected file type: $file_type"
        fi
    else
        echo "✗ Failed to download from URL $counter"
        # Remove any partially downloaded file
        [ -f "$filepath" ] && rm "$filepath"
    fi
    
    echo ""
    ((counter++))
    
done < "$WGET_FILE"

echo "Download process completed!"
echo "Total URLs processed: $((counter-1))"
echo "Check the $CV_DIR directory for downloaded files."

# List downloaded files
echo ""
echo "Files in CVs directory:"
ls -la "$CV_DIR"
