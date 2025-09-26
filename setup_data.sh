#!/bin/bash
# Copy data file for local testing

echo "📂 Setting up data file for local testing..."

SOURCE_FILE="../dataops-foundation-jenkins/data/LoanStats_web_small.csv"
TARGET_DIR="data"
TARGET_FILE="$TARGET_DIR/LoanStats_web_small.csv"

if [ -f "$SOURCE_FILE" ]; then
    echo "✅ Source file found: $SOURCE_FILE"
    
    # Create data directory if not exists
    mkdir -p "$TARGET_DIR"
    
    # Copy file
    cp "$SOURCE_FILE" "$TARGET_FILE"
    
    if [ -f "$TARGET_FILE" ]; then
        echo "✅ Data file copied successfully to: $TARGET_FILE"
        file_size=$(stat -c%s "$TARGET_FILE" 2>/dev/null || stat -f%z "$TARGET_FILE" 2>/dev/null)
        echo "📊 File size: $file_size bytes"
    else
        echo "❌ Failed to copy data file"
        exit 1
    fi
else
    echo "❌ Source file not found: $SOURCE_FILE"
    echo "💡 Please ensure the original project exists at the correct path"
    exit 1
fi

echo "🎉 Data setup complete!"
