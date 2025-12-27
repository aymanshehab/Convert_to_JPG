# Convert_to_JPG

A simple Python GUI tool for Ubuntu 24.04 to batch convert images into JPG format. It automatically handles transparency by flattening images onto a solid white background.

## Ubuntu 24.04 Requirements
Ubuntu does not include the necessary GUI components by default. Run this command first:

```bash
sudo apt update && sudo apt install python3-tk -y
```

## Installation
Install the image processing library:

```bash
pip install Pillow
```

## How to Use
1. Run the script:
```bash
python3 Convert_to_JPG.py
```
2. Select the Input Folder containing your source images.

3. Select the Output Folder for your new JPG files.

4. Click Start Conversion.

## Features
- Transparency Handling: Automatically replaces transparent layers with white.

- Format Support: PNG, WebP, TIFF, BMP, GIF, and more.

- Multithreaded: The GUI remains active while images are being processed.

- Progress Tracking: Includes a visual progress bar and file counter.

## License
Convert_to_JPG
Copyright (C) 2025 Ayman Ali Shehab

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.