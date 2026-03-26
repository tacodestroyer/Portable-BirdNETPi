BirdNET-Pi ePaper Display (2.13" / 2.9")

A lightweight add-on for BirdNET-Pi that displays real-time bird detection statistics on a Waveshare ePaper HAT using a Raspberry Pi.

This project reads directly from the BirdNET-Pi SQLite database and renders key daily stats to a low-power ePaper display — perfect for a clean, always-on “bird activity dashboard”.

Throw all of this into this case and you'll be set with a portable unit!
https://makerworld.com/en/models/1336154-portable-pi-sdr-case

- Features
	- Last Detected Species
	- Top Species of the Day (Top 3 or Top 5)
	- Total Detections Today
	- Live Timestamp Updates
	- Low power usage (ideal for always-on display setups)
- Supported Hardware
	- Raspberry Pi (tested on Pi 4)
	- Waveshare ePaper HAT:
		- 2.13" (V2 / V3)
		- 2.9" (V2 / V3 recommended)

**How It Works**

This script:

Connects to the BirdNET-Pi SQLite database
Queries detection data (latest detection, daily counts, top species)
Renders a formatted dashboard using Pillow
Pushes the image to the ePaper display via SPI

The display refreshes at a configurable interval (default: 2–3 minutes) to balance responsiveness and panel longevity.

**Data Source**

The script reads from the detections table in BirdNET-Pi:

Com_Name – Common name of species
Date / Time – Detection timestamp
Confidence – Detection confidence score

No modifications are made to the BirdNET-Pi system — this is a read-only integration.

**Installation**
Clone this repo onto your Raspberry Pi

Install dependencies:

sudo apt install python3-pil python3-spidev
pip3 install pillow

Clone Waveshare drivers:

git clone https://github.com/waveshare/e-Paper.git
Update the script:
Set your DB_PATH
Select the correct ePaper driver (e.g. epd2in13_V3, epd2in9_V3)

**Run:**

python3 birdnet-epaper.py
Optional: Run at Startup

Use a systemd service to automatically start the display on boot.

Built as a companion display for BirdNET-Pi to provide a glanceable, ambient view of local bird activity without needing to open the web interface.
