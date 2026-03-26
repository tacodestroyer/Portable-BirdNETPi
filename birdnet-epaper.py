#!/usr/bin/env python3

import sys
import time
import sqlite3
from datetime import datetime, date
from PIL import Image, ImageDraw, ImageFont

# ==== WAVESHARE DRIVER PATH ====
sys.path.append('/home/taco/e-Paper/RaspberryPi_JetsonNano/python/lib')
from waveshare_epd import epd2in9_V2

# ==== CONFIG ====
DB_PATH = "/home/taco/BirdNET-Pi/scripts/birds.db"
REFRESH_SECONDS = 180

FONT_TITLE = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18
)
FONT_BODY = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13
)
FONT_SMALL = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
)

# ==== DATABASE QUERIES ====
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = date.today().isoformat()

    # Last detected species (most recent Date + Time)
    cursor.execute("""
        SELECT Com_Name
        FROM detections
        ORDER BY Date DESC, Time DESC
        LIMIT 1
    """)
    last_species = cursor.fetchone()
    last_species = last_species[0] if last_species else "None"

    # Daily Top 3 species
    cursor.execute("""
        SELECT Com_Name, COUNT(*) AS cnt
        FROM detections
        WHERE Date = ?
        GROUP BY Com_Name
        ORDER BY cnt DESC
        LIMIT 3
    """, (today,))
    top3 = cursor.fetchall()

    # Total detections today
    cursor.execute("""
        SELECT COUNT(*)
        FROM detections
        WHERE Date = ?
    """, (today,))
    total_today = cursor.fetchone()[0]

    conn.close()
    return last_species, top3, total_today

# ==== DISPLAY RENDER ====
def truncate(text, max_chars):
    return text if len(text) <= max_chars else text[:max_chars - 1] + "…"

def render(epd, last, top3, total):
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    y = 0

    # Title
    draw.text((2, y), "BirdNET-Pi", font=FONT_TITLE, fill=0)
    y += 18

    # Last detected
    draw.text(
        (2, y),
        f"Last: {truncate(last, 28)}",
        font=FONT_BODY,
        fill=0
    )
    y += 14

    # Top 3 header
    draw.text((2, y), "Top 3 Today", font=FONT_BODY, fill=0)
    y += 12

    # Top 3 list
    for i, (species, count) in enumerate(top3, 1):
        line = f"{i}. {truncate(species, 22)} ({count})"
        draw.text((6, y), line, font=FONT_SMALL, fill=0)
        y += 11

    # Total today
    y += 2
    draw.text(
        (2, y),
        f"Total Today: {total}",
        font=FONT_BODY,
        fill=0
    )

    # Footer time
    draw.text(
        (2, epd.height - 12),
        datetime.now().strftime("%H:%M %m/%d"),
        font=FONT_SMALL,
        fill=0
    )

    image = image.rotate(180,expand=True)
    epd.display(epd.getbuffer(image))

# ==== MAIN LOOP ====
def main():
    epd = epd2in9_V2.EPD()
    epd.init()
    epd.Clear(0xFF)

    try:
        while True:
            last, top3, total = get_stats()
            render(epd, last, top3, total)
            time.sleep(REFRESH_SECONDS)

    except KeyboardInterrupt:
        epd.sleep()
        epd.Dev_exit()

if __name__ == "__main__":
    main()
