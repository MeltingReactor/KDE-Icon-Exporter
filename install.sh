#!/bin/bash
set -euo pipefail

declare -A packages=(
    ["^python3([0-9]{0,2})?$"]="python3"
    ["^qt6$"]="qt6-qtbase-devel"
    ["^kdialog$"]="kdialog"
    ["^git$"]="git"
)

failures=()

check_and_install() {
    local pattern="$1"
    local pkg="$2"

    # Only install if not present
    if ! dnf list installed 2>/dev/null | grep -E "$pattern" &>/dev/null; then
        echo "Installing $pkg..."
        if ! sudo dnf install -y "$pkg"; then
            failures+=("$pkg")
        fi
    fi
}

for pattern in "${!packages[@]}"; do
    check_and_install "$pattern" "${packages[$pattern]}"
done

if [ ${#failures[@]} -eq 0 ]; then
    echo "✅ Dependencies are installed successfully."
else
    echo "❌ Failed to install: ${failures[*]}"
    exit 1
fi

REPO_URL="https://github.com/MeltingReactor/KDE-Icon-Exporter.git"
CLONE_DIR="KDEiconExporter"

if [ -d "$CLONE_DIR" ]; then
    echo "Directory $CLONE_DIR already exists. Skipping clone."
else
    echo "Cloning repository..."
    if ! git clone "$REPO_URL" "$CLONE_DIR"; then
        echo "❌ Git error."
        exit 1
    fi
fi

# -------------------------------
# Create start.sh
# -------------------------------
cd "$CLONE_DIR" || { echo "❌ Bash error"; exit 1; }
echo "python3 main.py" > start.sh
chmod +x start.sh

echo "✅ Installation finished."
