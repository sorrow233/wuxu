
import plistlib
import base64
from PIL import Image
import io
import sys
import os

def check_cape_image_size(cape_path):
    print(f"Checking {cape_path}...")
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        cursors = plist_data.get('Cursors', {})
        if not cursors:
            print("No cursors found")
            return
            
        first_cursor = list(cursors.values())[0]
        representations = first_cursor.get('Representations', [])
        
        if not representations:
            print("No representations found")
            return

        # Get first frame data
        image_data = representations[0]
        
        img = Image.open(io.BytesIO(image_data))
        print(f"Image Size inside Cape: {img.size}")
        
        points_high = first_cursor.get('PointsHigh', 0)
        print(f"PointsHigh setting: {points_high}")
        
        scale = img.height / points_high if points_high else 0
        print(f"Calculated Scale: {scale}x")
        
        if scale >= 2.0:
            print("Verdict: HD/Retina")
        else:
            print("Verdict: SD (Standard)")
            
    except Exception as e:
        print(f"Error: {e}")

if len(sys.argv) > 1:
    check_cape_image_size(sys.argv[1])
else:
    print("Please provide file path")
