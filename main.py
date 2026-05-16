import sys
import os
import requests
import json
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon

# Set your FreeConvert token here, or leave as None to skip SVG conversion
FREECONVERT_TOKEN = None  # "YOUR_ACCESS_TOKEN_HERE"

class IconExporter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KDE Icon Exporter (PNG / Optional SVG)")
        self.setGeometry(300, 300, 400, 180)

        layout = QVBoxLayout()

        self.label = QLabel("Enter KDE Icon Name:")
        layout.addWidget(self.label)

        self.icon_name_input = QLineEdit()
        layout.addWidget(self.icon_name_input)

        self.button_export = QPushButton("Export Icon")
        self.button_export.clicked.connect(self.export_icon)
        layout.addWidget(self.button_export)

        self.setLayout(layout)

    def export_icon(self):
        icon_name = self.icon_name_input.text().strip()
        if not icon_name:
            QMessageBox.warning(self, "Error", "Please enter an icon name")
            return

        icon = QIcon.fromTheme(icon_name)
        if icon.isNull():
            QMessageBox.warning(self, "Error", f"Icon '{icon_name}' not found in current theme.")
            return

        # Pick largest available size
        sizes = icon.availableSizes()
        size = max(max(s.width(), s.height()) for s in sizes) if sizes else 512

        # Render icon to PNG
        pixmap = icon.pixmap(size, size)
        png_file = f"{icon_name}.png"
        pixmap.save(png_file)

        if FREECONVERT_TOKEN:
            # Convert PNG to colored SVG using FreeConvert
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {FREECONVERT_TOKEN}'
            }

            input_body = {
                "tasks": {
                    "import-1": {"operation": "import/upload"},
                    "convert-1": {
                        "operation": "convert",
                        "input": "import-1",
                        "input_format": "png",
                        "output_format": "svg",
                        "options": {
                            "color-mode": "color",
                            "color-precision": 8,
                            "gradient-step": 16,
                            "filter-speckle": 4
                        }
                    },
                    "export-1": {
                        "operation": "export/url",
                        "input": ["convert-1"],
                        "filename": f"{icon_name}.svg"
                    }
                }
            }

            # Step 1: create job
            response = requests.post("https://api.freeconvert.com/v1/process/jobs",
                                     data=json.dumps(input_body), headers=headers)
            if response.status_code != 200:
                QMessageBox.warning(self, "Error", f"FreeConvert job creation failed: {response.text}")
                return
            response_json = response.json()
            job_id = response_json["id"]

            # Step 2: upload PNG
            upload_url = response_json["tasks"]["import-1"]["result"]["form"]["url"]
            upload_fields = response_json["tasks"]["import-1"]["result"]["form"]["parameters"]
            with open(png_file, "rb") as f:
                files = {"file": f}
                upload_resp = requests.post(upload_url, data=upload_fields, files=files)
                if upload_resp.status_code != 204:
                    QMessageBox.warning(self, "Error", f"Upload failed: {upload_resp.text}")
                    return

            # Step 3: poll for job completion
            job_status_url = f"https://api.freeconvert.com/v1/process/jobs/{job_id}"
            while True:
                status_resp = requests.get(job_status_url, headers=headers)
                status_json = status_resp.json()
                if status_json["status"] == "finished":
                    break
                elif status_json["status"] == "error":
                    QMessageBox.warning(self, "Error", "FreeConvert job failed.")
                    return
                time.sleep(1)

            # Step 4: download SVG
            export_url = status_json["tasks"]["export-1"]["result"]["files"][0]["url"]
            svg_resp = requests.get(export_url)
            if svg_resp.status_code == 200:
                svg_file = f"{icon_name}.svg"
                with open(svg_file, "wb") as f:
                    f.write(svg_resp.content)
                QMessageBox.information(self, "Success", f"Saved PNG: '{png_file}'\nColored SVG: '{svg_file}'")
            else:
                QMessageBox.warning(self, "Error", "Failed to download SVG from FreeConvert.")
        else:
            QMessageBox.information(self, "Success", f"Saved PNG: '{png_file}'\n(No token set, SVG skipped)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconExporter()
    window.show()
    sys.exit(app.exec())
