
import plistlib
import base64
from PIL import Image
import io
import sys

def check_cape_image_size(cape_path):
    print(f"Checking {cape_path}...")
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        cursors = plist_data.get('Cursors', {})
        first_cursor = list(cursors.values())[0]
        representations = first_cursor.get('Representations', [])
        
        if not representations:
            print("No representations found")
            return

        # Get first frame data
        image_data = representations[0]
        
        # If it's bytes, good. If base64 string, decode. Plistlib usually gives bytes.
        
        img = Image.open(io.BytesIO(image_data))
        print(f"Image Size inside Cape: {img.size}")
        
        points_high = first_cursor.get('PointsHigh', 0)
        print(f"PointsHigh setting: {points_high}")
        
        scale = img.height / points_high if points_high else 0
        print(f"Calculated Scale: {scale}x")
        
    except Exception as e:
        print(f"Error: {e}")

check_cape_image_size("/Users/kang/Downloads/MYGO母鸡卡指针合集/MYGO_Cape_Output/Chihaya_Anon_千早爱音.cape")
