#!/bin/bash
set -e

declare -A packages=(
    ["python3([0-9]{0,2})?"]="python3"
    ["qt6"]="qt6-qtbase-devel"
    ["kdialog"]="kdialog"
    ["git"]="git"
)

failures=()

check_and_install() {
    local pattern="$1"
    local pkg="$2"

    if ! dnf list installed 2>/dev/null | grep -E "^$pattern" &>/dev/null; then
        if ! sudo dnf install -y "$pkg"; then
            failures+=("$pkg")
        fi
    fi
}

for pattern in "${!packages[@]}"; do
    check_and_install "$pattern" "${packages[$pattern]}"
done

if [ ${#failures[@]} -eq 0 ]; then
    echo "Dependencies are installed successfully."
else
    echo "The following dependencies failed to install: ${failures[*]} ❌"
fi

REPO_URL="https://github.com/user/test.git"  # Replace with actual repo URL
CLONE_DIR="KDEiconExporter"

if git clone "$REPO_URL" "$CLONE_DIR"; then
    cd "$CLONE_DIR" || { echo "Git error."; exit 1; }

    # Create start.sh with content
    echo "python3 main.py" > start.sh
    chmod +x start.sh

    echo "Installation finished."
else
    echo "Git error."
    exit 1
fi
