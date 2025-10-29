#!/bin/bash

# PolyRAG Language Configuration Script
# This script helps configure the default language for the PolyRAG application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if .env file exists
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    print_error ".env file not found!"
    print_info "Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created"
    else
        print_error "No .env.example file found. Please create a .env file manually."
        exit 1
    fi
fi

echo ""
echo "======================================"
echo "  PolyRAG Language Configuration"
echo "======================================"
echo ""

# Display current language setting
CURRENT_LANG=$(grep "^LANGUAGE=" "$ENV_FILE" | cut -d '=' -f2 || echo "not set")
print_info "Current language setting: ${CURRENT_LANG}"
echo ""

# Display available languages
echo "Available languages:"
echo "  1) English (en/english)"
echo "  2) Arabic (ar/arabic) - RTL support"
echo "  q) Quit without changes"
echo ""

# Get user choice
read -p "Select language (1-2, or q to quit): " choice

case $choice in
    1)
        NEW_LANG="english"
        DISPLAY_NAME="English"
        ;;
    2)
        NEW_LANG="arabic"
        DISPLAY_NAME="Arabic (العربية)"
        ;;
    q|Q)
        print_info "No changes made. Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
print_info "Setting language to: ${DISPLAY_NAME}"

# Update or add LANGUAGE variable in .env file
if grep -q "^LANGUAGE=" "$ENV_FILE"; then
    # Update existing LANGUAGE line
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/^LANGUAGE=.*/LANGUAGE=${NEW_LANG}/" "$ENV_FILE"
    else
        # Linux
        sed -i "s/^LANGUAGE=.*/LANGUAGE=${NEW_LANG}/" "$ENV_FILE"
    fi
    print_success "Updated LANGUAGE setting in .env"
else
    # Add LANGUAGE variable
    echo "LANGUAGE=${NEW_LANG}" >> "$ENV_FILE"
    print_success "Added LANGUAGE setting to .env"
fi

echo ""
print_success "Language configuration complete!"
echo ""
print_info "Next steps:"
echo "  1. Restart your PolyRAG application"
echo "  2. The UI will now display in ${DISPLAY_NAME}"
echo "  3. Users can still change language using the sidebar selector"
echo ""

# Check if language file exists
LANG_FILE=".variables/demo_fully_rag/display_texts"
if [ "$NEW_LANG" = "arabic" ]; then
    LANG_FILE="${LANG_FILE}.ar.json"
elif [ "$NEW_LANG" = "english" ]; then
    LANG_FILE="${LANG_FILE}.json"
fi

if [ -f "$LANG_FILE" ]; then
    print_success "Language file found: ${LANG_FILE}"
else
    print_warning "Language file not found: ${LANG_FILE}"
    print_info "Make sure the language file exists before starting the application"
fi

echo ""
print_info "To restart the application:"
echo "  • Docker: docker-compose restart"
echo "  • Local: Stop and restart your Streamlit server"
echo ""
